import pygame
import random
from Settings import *
from os import path
vec = pygame.math.Vector2

# Class
def init_sprite(sprite, game, dict, object, group, parent):
    sprite.game = game
    sprite.groups = sprite.game.all_sprites, group
    sprite.object = object
    sprite.group = group
    sprite.parent = parent
    sprite.dt = game.dt
    init_dict(sprite, dict, object), init_vec(sprite), init_image(sprite), sprite.init_settings()
    update_center(sprite)
    pygame.sprite.Sprite.__init__(sprite, sprite.groups)

def init_dict(sprite, dict, object):
    sprite.dict = dict
    sprite.object_dict = sprite.dict[object]
    sprite.game_dict = sprite.game.game_dict

def init_vec(sprite):
    sprite.pos = vec(sprite.object_dict["pos"][:])
    sprite.range = sprite.object_dict["range"][:]
    sprite.move = sprite.object_dict["move"]
    if sprite.move:
        sprite.pos_dt = vec(0, 0)
        sprite.vel = vec(0, 0)
        sprite.move_speed = vec(sprite.object_dict["move_speed"])
        if "debug_move_speed" in sprite.object_dict:
            sprite.debug_move_speed = vec(sprite.object_dict["debug_move_speed"])
        else:
            sprite.debug_move_speed = sprite.move_speed

def init_image(sprite):
    # Settings
    sprite._layer = sprite.dict["layer"]
    sprite.image = sprite.object_dict["image"]
    sprite.center = sprite.object_dict["center"]
    sprite.bobbing = sprite.object_dict["bobbing"]
    sprite.flip = sprite.object_dict["flip"]
    sprite.impact = sprite.object_dict["impact"]

    # Image
    sprite.table = sprite.object_dict["table"]
    if sprite.table:
        sprite.reverse = sprite.object_dict["reverse"]
        sprite.size = sprite.object_dict["size"]
        sprite.side = sprite.object_dict["side"]
        sprite.animation_time = sprite.object_dict["animation_time"]
        sprite.animation_loop = sprite.object_dict["animation_loop"]
        sprite.loop = 0
        sprite.index = 0
        sprite.current_time = 0
        sprite.images_side = load_tile_table(path.join(sprite.game.graphics_folder, sprite.image), sprite.size[0], sprite.size[1], sprite.reverse)
        sprite.images = sprite.images_side[sprite.side]
        sprite.image = sprite.images[sprite.index]
    else:
        sprite.image = load_image(sprite.game.graphics_folder, sprite.image)
    sprite.rect = sprite.image.get_rect()

    # Center
    if sprite.center:
        sprite.rect.center = sprite.pos

    # Bobbing
    if sprite.bobbing:
        sprite.tween = tween.linear
        sprite.step = 0
        sprite.dir = 1

    # Flip
    if sprite.flip:
        if sprite.table:
            for side in range(len(sprite.images_side)):
                for index in range(len(sprite.images_side[side])):
                    sprite.images_side[side][index] = pygame.transform.flip(sprite.images_side[side][index], True, False)
                    sprite.image = sprite.images[sprite.index]
        else:
            sprite.image = pygame.transform.flip(sprite.image, True, False)



def update_time_dependent(sprite):
    if sprite.table:
        sprite.current_time += sprite.dt
        if sprite.current_time >= sprite.animation_time:
            if sprite.index == len(sprite.images)-1:
                sprite.loop += 1
            sprite.current_time = 0
            sprite.index = (sprite.index + 1) % len(sprite.images)
            sprite.image = sprite.images[sprite.index]
        if sprite.animation_loop and sprite.index == 0 and sprite.loop != 0:
            sprite.kill()
        sprite.image = pygame.transform.rotate(sprite.image, 0)


def update_center(sprite):
    if sprite.center:
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = sprite.pos


def update_bobbing(sprite):
    if sprite.bobbing:
        offset = BOB_RANGE * (sprite.tween(sprite.step / BOB_RANGE) - 0.5)
        sprite.rect.centery = sprite.pos.y + offset * sprite.dir
        sprite.step += BOB_SPEED
        if sprite.step > BOB_RANGE:
            sprite.step = 0
            sprite.dir *= -1



# Gameplay / Interface
def init_character(sprite):
    # Position
    sprite.grid_size = sprite.game_dict["grid_size"]
    sprite.grid_pos = vec(sprite.object_dict["grid_pos"][:])
    sprite.grid_dt = vec(sprite.game_dict["grid_dt"])

    # Status
    sprite.name = sprite.object_dict["name"]
    sprite.level = sprite.object_dict["level"]
    sprite.max_health = sprite.object_dict["max_health"]
    sprite.health_regen = sprite.object_dict["health_regen"]
    sprite.health = sprite.max_health
    sprite.max_mana = sprite.object_dict["max_mana"]
    sprite.mana_regen = sprite.object_dict["mana_regen"]
    sprite.mana = sprite.max_mana
    sprite.max_energy = sprite.object_dict["max_energy"]
    sprite.energy_regen = sprite.object_dict["energy_regen"]
    sprite.energy = sprite.max_energy

def init_interface(sprite):
    # Interface
    sprite.ui_font = sprite.game_dict["ui_font"]
    sprite.ui_size = sprite.game_dict["ui_size"]
    sprite.ui_color = sprite.game_dict["ui_color"]
    sprite.status_font = sprite.game_dict["status_font"]
    sprite.status_size = sprite.game_dict["status_size"]
    sprite.status_color = sprite.game_dict["status_color"]
    sprite.hp_offset = sprite.object_dict["hp_offset"][:]

    # Debug
    sprite.debug_color = sprite.object_dict["debug_color"]
    sprite.debug_pos = sprite.object_dict["debug_pos"]
    sprite.debug_dt = sprite.object_dict["debug_dt"]

def update_move(sprite):
    if sprite.vel == (0, 0):
        if not sprite.game.debug_mode:
            sprite.vel = vec(sprite.move_speed.elementwise() * sprite.range[0])
        else:
            sprite.vel = vec(sprite.debug_move_speed.elementwise() * sprite.range[0])
    if abs(sprite.pos_dt[0] + sprite.vel.x * sprite.dt) <= sprite.grid_dt[0] and abs(
            sprite.pos_dt[1] + sprite.vel.y * sprite.dt) <= sprite.grid_dt[1]:
        sprite.pos += sprite.vel * sprite.dt
        sprite.pos_dt += sprite.vel.x * sprite.dt, sprite.vel.y * sprite.dt
    else:
        sprite.grid_pos += sprite.range[0]
        sprite.pos = vec(sprite.pos - sprite.pos_dt + sprite.grid_dt.elementwise() * sprite.range[0])
        sprite.pos_dt = vec(0, 0)
        sprite.vel = vec(0, 0)
        del sprite.range[0]

def init_spell(spell, key, game, dict, object=None, group=None, parent=None):
    if parent.cooldown[key] <= 0 and parent.mana - game.spell_dict[object]["mana_cost"] >= 0 and parent.energy - game.spell_dict[object]["energy_cost"] >= 0:
        parent.cooldown[key] += game.spell_dict[object]["cooldown"]
        parent.mana -= game.spell_dict[object]["mana_cost"]
        parent.energy -= game.spell_dict[object]["energy_cost"]
        parent.last_attack = pygame.time.get_ticks()
        spell(game, dict, object, group, parent)

# Draw
def draw_interface(game):
    # Background
    game.gameDisplay.fill(game.background_color)
    game.gameDisplay.blit(game.background_image, (0, 0))

    # Interface
    for sprite in game.characters:
        # Grid Pos
        pygame.draw.rect(game.gameDisplay, sprite.debug_color, (sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0], sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1], sprite.debug_dt[0], sprite.debug_dt[1]))
        sprite.draw_ui()

    pygame.draw.rect(game.gameDisplay, game.game_dict["color"]["cursor"], (game.player.debug_pos[0] + (game.player.grid_pos[0]+4) * game.player.grid_dt[0], game.player.debug_pos[1] + game.player.grid_pos[1] * game.player.grid_dt[1], game.player.debug_dt[0], game.player.debug_dt[1]))


def draw_debug(game):
    # Debug
    if game.debug_mode:
        for sprite in game.all_sprites:
            pygame.draw.rect(game.gameDisplay, game.debug_color, sprite.rect, 1)
        for sprite in game.characters:
            sprite.draw_debug()
            pygame.draw.rect(game.gameDisplay, sprite.debug_color, (sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0], sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1], sprite.debug_dt[0], sprite.debug_dt[1]), 1)

def draw_sprite(game):
    for sprite in game.all_sprites:
        game.gameDisplay.blit(sprite.image, sprite)

def draw_status(game):
    for sprite in game.characters:
        sprite.draw_status()
        game.draw_text(sprite.health, sprite.status_font, sprite.status_size, sprite.status_color, sprite.pos + sprite.hp_offset, "center", game.debug_mode)


# Miscellaneous
def load_file(path, image=False):
    file = []
    for file_name in os.listdir(path):
        if image:
            file.append(pygame.image.load(path + os.sep + file_name).convert_alpha())
        else:
            file.append(path + os.sep + file_name)
    return file


def load_image(image_path, image_directory):
    if isinstance(image_directory, list):
        images = []
        for image in image_directory:
            images.append(pygame.image.load(path.join(image_path, image)).convert_alpha())
        return images
    else:
        return pygame.image.load(path.join(image_path, image_directory)).convert_alpha()


def load_tile_table(filename, width, height, reverse, colorkey=(0, 0, 0)):
    image = pygame.image.load(filename).convert_alpha()
    image.set_colorkey(colorkey)
    image_width, image_height = image.get_size()
    tile_table = []
    if not reverse:
        for tile_y in range(int(image_height / height)):
            line = []
            tile_table.append(line)
            for tile_x in range(int(image_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
    else:
        for tile_x in range(int(image_width / width)):
            column = []
            tile_table.append(column)
            for tile_y in range(int(image_height / height)):
                rect = (tile_x * width, tile_y * height, width, height)
                column.append(image.subsurface(rect))
    return tile_table


def transparent_surface(width, height, color, border, colorkey=(0, 0, 0)):
    surface = pygame.Surface((width, height)).convert()
    surface.set_colorkey(colorkey)
    surface.fill(color)
    surface.fill(colorkey, surface.get_rect().inflate(-border, -border))
    return surface


def sort_list(list, var, reverse=False):
    if reverse:
        list.reverse()

    for i in range(len(list)):
        # Display list
        #print(list)

        if list[i] == var:
            cpt = 0
            while list[i + cpt] == var and i + cpt < len(list)-1:
                cpt += 1
            list[i] = list[i+cpt]
            list[i+cpt] = var

    if reverse:
        list.reverse()
