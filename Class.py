import pygame
import pytweening as tween
import random

from Settings import *
from Function import *
vec = pygame.math.Vector2


PLACEHOLDER = 32

"""
    Others Functions
"""
class Cursor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, x_dt, y_dt, width=CURSOR_WIDTH, height=CURSOR_HEIGHT, color=CURSOR_COLOR, center=True):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = LAYER_CURSOR
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Position
        self.pos = [x, y]
        self.pos_dt = [x_dt, y_dt]

        # Surface
        self.image = transparent_surface(width, height, color, 6)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = center
        if self.center:
            self.rect.center = self.pos

    def move(self, dx=0, dy=0):
        self.pos[0] += dx * self.pos_dt[0]
        self.pos[1] += dy * self.pos_dt[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.center:
            self.rect.center = self.pos



class Spell(pygame.sprite.Sprite):
    def __init__(self, game, dict, game_dict=None, object=None, character=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.spell
        self._layer = dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.character = character
        self.init_dict(dict, game_dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

        # Settings
        self.spawn_time = pygame.time.get_ticks()

    def init_dict(self, dict, game_dict, object):
        self.dict = dict
        self.game_dict = game_dict
        self.object_dict = self.dict[object]

    def init_settings(self):
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.character.grid_pos[:]
        self.range = self.object_dict["range"][:]

    def init_vec(self):
        self.offset = self.dict["offset"]
        self.cast_offset = self.dict["cast_offset"]
        self.pos = vec(self.game_dict["pos"]["player"][0] + self.grid_pos[0] * self.grid_dt[0] + self.offset[0] + self.cast_offset[0],
                       self.game_dict["pos"]["player"][1] + self.grid_pos[1] * self.grid_dt[1] + self.offset[1] + self.cast_offset[1])
        self.pos_dt = vec(0, 0)
        self.vel = vec(0, 0)
        self.speed = vec(self.object_dict["speed"])

    def init_image(self):
        self.image = self.object_dict["image"]
        self.table = self.object_dict["table"]
        self.size = self.object_dict["size"]
        self.side = self.object_dict["side"]
        self.center = self.object_dict["center"]
        self.bobbing = self.object_dict["bobbing"]
        self.animation_time = self.object_dict["animation_time"]

        # Image
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1])
            self.images = self.images_side[self.side]
            self.image = self.images[self.index]
            self.current_time = 0
        else:
            self.image = load_image(self.game.graphics_folder, self.image)
        self.rect = self.image.get_rect()

        # Center
        if self.center:
            self.rect.center = self.pos

        # Bobbing
        if self.bobbing:
            self.tween = tween.linear
            self.step = 0
            self.dir = 1

    def move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < 2 * self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < 2 * self.grid_size[1]:
                if self.vel == (0, 0):
                    self.pos_dt[0] = self.game_dict["pos"]["player"][0] + (self.grid_pos[0] + self.range[0][0]) * self.grid_dt[0] - self.pos[0]
                    self.pos_dt[1] = self.game_dict["pos"]["player"][1] + (self.grid_pos[1] + self.range[0][1]) * self.grid_dt[1] - self.pos[1]
                    self.vel.x = self.range[0][0] * self.speed[0]
                    self.vel.y = self.range[0][1] * self.speed[1]

                if self.range[0][0] * self.pos_dt[0] > 0 or self.range[0][1] * self.pos_dt[1] > 0:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt -= self.vel * self.game.dt
                else:
                    self.grid_pos[0] += self.range[0][0]
                    self.grid_pos[1] += self.range[0][1]
                    self.pos[0] = self.game_dict["pos"]["player"][0] + self.grid_pos[0] * self.grid_dt[0] + self.offset[0]
                    self.pos[1] = self.game_dict["pos"]["player"][1] + self.grid_pos[1] * self.grid_dt[1] + self.offset[1]
                    self.pos_dt = vec(0, 0)
                    self.vel = vec(0, 0)
                    del self.range[0]
            else:
                self.kill()
        else:
            self.kill()

    def update(self):
        self.move()
        self.game.update_sprite(self)
        if pygame.time.get_ticks() - self.spawn_time > 2500:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, game, dict, game_dict=None, character="player"):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.dict, self.char_dict, self.game_dict = dict, dict[character], game_dict
        self.init_dict()
        self.dt = game.dt

        # Vector
        self.pos = vec(self.pos)
        self.pos_dt = vec(0, 0)
        self.vel = vec(0, 0)
        self.d_pos = []

        # Image
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1])
            self.images = self.images_side[self.side]
            self.image = self.images[self.index]
            self.current_time = 0
        else:
            self.image = load_image(self.game.graphics_folder, self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        if self.center:
            self.rect.center = self.pos

        # Bobbing
        if self.bobbing:
            self.tween = tween.linear
            self.step = 0
            self.dir = 1

    def init_dict(self):
        self.center = self.dict["center"]
        self.bobbing = self.dict["bobbing"]

        self.name = self.char_dict["name"]
        self.pos = self.char_dict["pos"]
        self.grid_pos = self.char_dict["grid_pos"]
        self.table = self.char_dict["table"]

        self.image = self.char_dict["image"]
        self.size = self.char_dict["size"]
        self.side = self.char_dict["side"]
        self.animation_time = self.char_dict["animation_time"]

        self.level = self.char_dict["level"]
        self.max_health = self.char_dict["max_health"]
        self.health = self.char_dict["health"]
        self.max_mana = self.char_dict["max_mana"]
        self.mana = self.char_dict["mana"]

        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.movespeed = self.game_dict["movespeed"]
        self.spell_color = self.game_dict["color"]["spell"]

    def move(self, dx=0, dy=0):
        if len(self.d_pos) < 3:
            self.d_pos.append(vec(dx, dy))

    def update_move(self):
        if len(self.d_pos) > 0:
            if 0 <= self.grid_pos[0] + self.d_pos[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.d_pos[0][1] < self.grid_size[1]:
                if self.vel == (0, 0) and self.pos_dt == (0, 0):
                    self.pos_dt[0] = self.d_pos[0][0] * self.grid_dt[0]
                    self.pos_dt[1] = self.d_pos[0][1] * self.grid_dt[1]
                    self.vel = self.d_pos[0] * self.movespeed

                if self.d_pos[0][0] * self.pos_dt[0] > 0 or self.d_pos[0][1] * self.pos_dt[1] > 0:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt -= self.vel * self.game.dt
                else:
                    self.grid_pos += self.d_pos[0]
                    self.pos.x = self.char_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0]
                    self.pos.y = self.char_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1]
                    self.pos_dt = vec(0, 0)
                    self.vel = vec(0, 0)
                    del self.d_pos[0]
            else:
                del self.d_pos[0]

    def draw_debug_move(self):
        pos_x = 165 + self.grid_pos[0] * self.grid_dt[0]
        pos_y = 330 + self.grid_pos[1] * self.grid_dt[1]
        pygame.draw.rect(self.game.gameDisplay, RED, (pos_x, pos_y, 110, 60))

    def draw_ui(self):
        pass

    def update(self):
        self.update_move()
        self.game.update_sprite(self)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, dict, ui_dict=None, character="Skeleton"):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.dict = dict
        self.ui_dict = ui_dict
        self.name = character
        self.char_dict = self.dict[self.name]
        self.init_dict()

        # Image
        self.table = dict["table"]
        if self.table:
            image = load_tile_table(path.join(self.game.graphics_folder, self.char_dict["image"]), self.dict["tile_dt"][0], self.dict["tile_dt"][1])
            self.index = 0
            self.images_bottom = image[0]
            self.images_left = image[1]
            self.images_right = image[2]
            self.images_top = image[3]
            self.images = self.images_left
            self.image = self.images[self.index]
            self.dt = game.dt
            self.current_time = 0
            self.animation_time = 0.50
        else:
            self.image = load_image(self.game.graphics_folder, self.char_dict["image"])
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Icon
        self.icon = None
        if "icon" in self.char_dict:
            self.icon = load_image(self.game.graphics_folder, self.char_dict["icon"])
            self.rect_icon = self.icon.get_rect()
            self.rect_icon.x = self.icon_pos[0]
            self.rect_icon.y = self.icon_pos[1]

        # Center
        self.center = dict["center"]
        if self.center:
            self.rect.center = self.pos
            if self.icon is not None:
                self.rect_icon.center = self.icon_pos

        # Bobbing
        self.bobbing = dict["bobbing"]
        self.tween = tween.linear
        self.step = 0
        self.dir = 1

    def init_dict(self):
        # Independent of character
        self.pos = self.dict["pos"]
        self.pos_dt = self.dict["pos_dt"]
        self.icon_pos = self.dict["icon_pos"]
        self.grid_size = self.ui_dict["grid_size"]
        self.health_rect = self.dict["health_rect"]
        self.health_color = self.ui_dict["health"]
        self.mana_rect = self.dict["mana_rect"]
        self.mana_dt = self.dict["mana_dt"]
        self.mana_color = self.ui_dict["mana"]
        self.status_font = self.ui_dict["status_font"]
        self.status_size = self.ui_dict["status_size"]
        self.status_color = self.ui_dict["status_color"]
        self.status_pos = self.ui_dict["status_enemy_pos"]

        # Dependent of character
        self.move_time = pygame.time.get_ticks()
        self.move_frequency = self.char_dict["move_frequency"]
        self.grid_pos = self.char_dict["grid_pos"]
        self.max_health = self.char_dict["max_health"]
        self.health = self.char_dict["health"]
        self.max_mana = self.char_dict["max_mana"]
        self.mana = self.char_dict["mana"]

    def move(self, dx=0, dy=0):
        if 0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]:
            self.pos[0] += dx * self.pos_dt[0]
            self.pos[1] += dy * self.pos_dt[1]
            self.grid_pos[0] += dx
            self.grid_pos[1] += dy
            return True
        else:
            return False

    def draw_status(self):
        # Text
        self.game.draw_text(self.name, self.status_font, self.status_size, self.status_color, self.status_pos[0], self.status_pos[1], align="center")
        if self.icon is not None:
            self.game.gameDisplay.blit(self.icon, self.rect_icon)

        # Health / Mana
        pygame.draw.rect(self.game.gameDisplay, self.health_color, (self.health_rect[0], self.health_rect[1] + (1 - self.health / self.max_health) * self.health_rect[3], self.health_rect[2], self.health/self.max_health * self.health_rect[3]))
        for i in range(int(self.mana)+1):
            pygame.draw.rect(self.game.gameDisplay, self.mana_color, (self.mana_rect[0] + i*self.mana_dt[0], self.mana_rect[1] + i*self.mana_dt[1] + (1-min(1, self.mana-i))*self.mana_rect[3], self.mana_rect[2], min(1, self.mana-i) * self.mana_rect[3]))

    def draw_ui(self):
        self.draw_status()

    def update_movement(self):
        if pygame.time.get_ticks() - self.move_time > self.move_frequency:
            dx = dy = 0
            while dx == dy == 0 or dx != 0 and dy != 0:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
            if self.move(dx, dy):
                self.move_time = pygame.time.get_ticks()
            else:
                self.update_movement()


    def update(self):
        self.game.update_sprite(self)
        self.update_movement()




class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dictionary, type, center=True, bobbing=False):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.items
        self._layer = LAYER_ITEMS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.dictionary = dictionary
        self.type = type

        # Position
        self.pos = [x, y]

        # Surface
        self.index = 0
        self.images = self.dictionary[self.type]
        self.table = isinstance(self.images, list)

        if self.table:
            self.image = self.dictionary[self.type][self.index]
        else:
            self.image = self.dictionary[self.type]

        # Rect
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = center
        if self.center:
            self.rect.center = self.pos

        # Time
        self.dt = game.dt
        self.current_time = 0
        self.animation_time = 0.50

        # Bobbing
        self.bobbing = bobbing
        self.tween = tween.linear
        self.step = 0
        self.dir = 1

    def update(self):
        self.game.update_sprite(self)
