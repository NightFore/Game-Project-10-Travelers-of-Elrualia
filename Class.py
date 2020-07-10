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
class Spell(pygame.sprite.Sprite):
    def __init__(self, game, dict, object=None, character=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.spell
        self._layer = self.game.spell_dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.character = character
        self.init_dict(dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

    def init_dict(self, dict, object):
        self.dict = dict
        self.object_dict = self.dict[object]
        self.game_dict = self.game.game_dict

    def init_settings(self):
        # Position
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.character.grid_pos[:]

        # Gameplay
        self.spawn_time = pygame.time.get_ticks()
        self.move = self.object_dict["move"]
        self.damage = self.object_dict["damage"]

    def init_vec(self):
        offset = [self.character.object_dict["spell_offset"][0] + self.character.object_dict["spell_cast_offset"][0] + self.character.pos_dt[0],
                  self.character.object_dict["spell_offset"][1] + self.character.object_dict["spell_cast_offset"][1]]
        self.pos = vec(self.game_dict["pos"]["player"][0] + self.grid_pos[0] * self.grid_dt[0] + offset[0],
                       self.game_dict["pos"]["player"][1] + self.grid_pos[1] * self.grid_dt[1] + offset[1])
        self.range = self.object_dict["range"][:]

        if self.move:
            self.move_speed = vec(self.object_dict["move_speed"])
            self.debug_move_speed = vec(self.object_dict["debug_move_speed"])
            self.pos_dt = vec(offset[0], 0)
            self.vel = vec(0, 0)

    def init_image(self):
        self.image = self.object_dict["image"]
        self.table = self.object_dict["table"]
        self.reverse = self.object_dict["reverse"]
        self.size = self.object_dict["size"]
        self.side = self.object_dict["side"]
        self.center = self.object_dict["center"]
        self.bobbing = self.object_dict["bobbing"]
        self.flip = self.object_dict["flip"]
        self.animation_time = self.object_dict["animation_time"]
        self.animation_loop = self.object_dict["animation_loop"]
        self.loop = 0

        # Image
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1], self.reverse)
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

        # Flip
        if self.flip:
            if self.table:
                for side in range(len(self.images_side)):
                    for index in range(len(self.images_side[side])):
                        self.images_side[side][index] = pygame.transform.flip(self.images_side[side][index], True, False)
                        self.image = self.images[self.index]
            else:
                self.image = pygame.transform.flip(self.image, True, False)

    def update_move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < 2 * self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < 2 * self.grid_size[1]:
                if self.vel == (0, 0):
                    if not self.game.debug_mode:
                        self.vel.x = self.move_speed[0] * self.range[0][0]
                        self.vel.y = self.move_speed[1] * self.range[0][1]
                    else:
                        self.vel.x = self.debug_move_speed[0] * self.range[0][0]
                        self.vel.y = self.debug_move_speed[1] * self.range[0][1]
                if abs(self.pos_dt[0] + self.vel.x * self.game.dt) <= self.grid_dt[0] and abs(self.pos_dt[1] + self.vel.y * self.game.dt) <= self.grid_dt[1]:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt[0] += self.vel.x * self.game.dt
                    self.pos_dt[1] += self.vel.y * self.game.dt
                else:
                    self.grid_pos[0] += self.range[0][0]
                    self.grid_pos[1] += self.range[0][1]
                    self.pos.x = self.pos.x - self.pos_dt[0] + self.grid_dt[0] * self.range[0][0]
                    self.pos.y = self.pos.y - self.pos_dt[1] + self.grid_dt[1] * self.range[0][1]
                    self.pos_dt = [0, 0]
                    self.vel = vec(0, 0)
            else:
                self.kill()
        else:
            self.kill()

    def collide_sprite(self):
        for sprite in self.game.characters:
            if self.character != sprite and (self.grid_pos[0] - self.grid_size[0] == sprite.grid_pos[0] and self.grid_pos[1] == sprite.grid_pos[1]):
                sprite.health -= self.damage
                Impact(self.game, self.object_dict, "impact_dict", self)
                self.kill()

    def update(self):
        self.game.update_sprite(self, move=self.move)

        self.collide_sprite()
        if pygame.time.get_ticks() - self.spawn_time > 2500:
            self.kill()


class Impact(pygame.sprite.Sprite):
    def __init__(self, game, dict, object="player", character=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.impact
        self._layer = self.game.character_dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.character = character
        self.init_dict(dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

    def init_dict(self, dict, object):
        self.dict = dict
        self.object_dict = self.dict[object]
        self.game_dict = self.game.game_dict

    def init_settings(self):
        # Position
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.character.grid_pos[:]

        # Gameplay
        self.spawn_time = pygame.time.get_ticks()

    def init_vec(self):
        self.pos = vec(self.character.pos)

    def init_image(self):
        self.image = self.object_dict["image"]
        self.table = self.object_dict["table"]
        self.reverse = self.object_dict["reverse"]
        self.size = self.object_dict["size"]
        self.side = self.object_dict["side"]
        self.center = self.object_dict["center"]
        self.bobbing = self.object_dict["bobbing"]
        self.flip = self.object_dict["flip"]
        self.animation_time = self.object_dict["animation_time"]
        self.animation_loop = self.object_dict["animation_loop"]
        self.loop = 0

        # Image
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1], self.reverse)
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

        # Flip
        if self.flip:
            if self.table:
                for side in range(len(self.images_side)):
                    for index in range(len(self.images_side[side])):
                        self.images_side[side][index] = pygame.transform.flip(self.images_side[side][index], True, False)
                        self.image = self.images[self.index]
            else:
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.game.update_sprite(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, game, dict, object="player", character=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = self.game.character_dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.character = character
        self.init_dict(dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

    def init_dict(self, dict, object):
        self.dict = dict
        self.object_dict = self.dict[object]
        self.game_dict = self.game.game_dict

    def init_settings(self):
        # Status
        self.name = self.object_dict["name"]
        self.level = self.object_dict["level"]
        self.max_health = self.object_dict["max_health"]
        self.health = self.object_dict["health"]
        self.max_mana = self.object_dict["max_mana"]
        self.mana = self.object_dict["mana"]

        # Position
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.object_dict["grid_pos"][:]

        # Interface
        self.hp_font = self.game_dict["hp_font"]
        self.hp_size = self.game_dict["hp_size"]
        self.hp_color = self.game_dict["hp_color"]
        self.hp_offset = self.object_dict["hp_offset"][:]

        # Debug
        self.debug_color = self.object_dict["debug_color"]
        self.debug_pos = self.object_dict["debug_pos"]
        self.debug_dt = self.object_dict["debug_dt"]

        # Gameplay
        self.last_attack = pygame.time.get_ticks()
        self.attack_rate = self.object_dict["attack_rate"]

    def init_vec(self):
        self.pos = vec(self.object_dict["pos"])
        self.pos_dt = [0, 0]
        self.vel = vec(0, 0)
        self.move_speed = self.object_dict["move_speed"]

        self.pos_reset = vec(self.object_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0], self.object_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1])
        self.range = []

    def init_image(self):
        self.image = self.object_dict["image"]
        self.table = self.object_dict["table"]
        self.reverse = self.object_dict["reverse"]
        self.size = self.object_dict["size"]
        self.side = self.object_dict["side"]
        self.center = self.object_dict["center"]
        self.bobbing = self.object_dict["bobbing"]
        self.flip = self.object_dict["flip"]
        self.animation_time = self.object_dict["animation_time"]
        self.animation_loop = self.object_dict["animation_loop"]
        self.loop = 0

        # Image
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1], self.reverse)
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

        # Flip
        if self.flip:
            if self.table:
                for side in range(len(self.images_side)):
                    for index in range(len(self.images_side[side])):
                        self.images_side[side][index] = pygame.transform.flip(self.images_side[side][index], True, False)
                        self.image = self.images[self.index]
            else:
                self.image = pygame.transform.flip(self.image, True, False)

    def update_move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < self.grid_size[1]:
                if self.vel == (0, 0):
                    self.vel.x = self.move_speed[0] * self.range[0][0]
                    self.vel.y = self.move_speed[1] * self.range[0][1]
                if abs(self.pos_dt[0] + self.vel.x * self.game.dt) <= self.grid_dt[0] and abs(self.pos_dt[1] + self.vel.y * self.game.dt) <= self.grid_dt[1]:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt[0] += self.vel.x * self.game.dt
                    self.pos_dt[1] += self.vel.y * self.game.dt
                else:
                    self.grid_pos[0] += self.range[0][0]
                    self.grid_pos[1] += self.range[0][1]
                    self.pos.x = self.pos.x - self.pos_dt[0] + self.grid_dt[0] * self.range[0][0]
                    self.pos.y = self.pos.y - self.pos_dt[1] + self.grid_dt[1] * self.range[0][1]
                    self.pos_dt = [0, 0]
                    self.vel = vec(0, 0)
                    del self.range[0]
            else:
                del self.range[0]

    def buffer_move(self, dx=0, dy=0):
        if len(self.range) < 2:
            self.range.append([dx, dy])

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x] or keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                Spell(self.game, self.game.spell_dict, "energy_ball", self)
                self.last_attack = pygame.time.get_ticks()
        if keys[pygame.K_c]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                Spell(self.game, self.game.spell_dict, "thunder", self)
                self.last_attack = pygame.time.get_ticks()

    def draw_ui(self):
        # Grid Pos
        pygame.draw.rect(self.game.gameDisplay, self.debug_color, (self.debug_pos[0] + self.grid_pos[0] * self.grid_dt[0], self.debug_pos[1] + self.grid_pos[1] * self.grid_dt[1], self.debug_dt[0], self.debug_dt[1]))

        # Cooldown
        pygame.draw.rect(self.game.gameDisplay, LIGHTGREY, (100, 620, 40, max(-40, -40 * (pygame.time.get_ticks() - self.last_attack) / self.attack_rate)))
        self.game.draw_text("X", None, 40, BLUE, 120, 600, "center", self.game.debug_mode)

    def draw_debug_mode(self):
        pygame.draw.rect(self.game.gameDisplay, CYAN, (self.debug_pos[0] + self.grid_pos[0] * self.grid_dt[0], self.debug_pos[1] + self.grid_pos[1] * self.grid_dt[1], self.debug_dt[0], self.debug_dt[1]), 1)
        pygame.draw.rect(self.game.gameDisplay, CYAN, (100, 620, 40, -40), 1)
        pygame.draw.rect(self.game.gameDisplay, CYAN, (100, 620, 40, max(-40, -40 * (pygame.time.get_ticks() - self.last_attack) / self.attack_rate)), 1)

    def draw_status(self):
        # Health
        self.game.draw_text(str(self.health), self.hp_font, self.hp_size, self.hp_color, int(self.pos[0] + self.hp_offset[0]), int(self.pos[1] + self.hp_offset[1]), "center", self.game.debug_mode)

    def update(self):
        self.game.update_sprite(self, move=True, keys=True)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, dict, object="player", character=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = self.game.character_dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.character = character
        self.init_dict(dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

    def init_dict(self, dict, object):
        self.dict = dict
        self.object_dict = self.dict[object]
        self.game_dict = self.game.game_dict

    def init_settings(self):
        # Status
        self.name = self.object_dict["name"]
        self.level = self.object_dict["level"]
        self.max_health = self.object_dict["max_health"]
        self.health = self.object_dict["health"]
        self.max_mana = self.object_dict["max_mana"]
        self.mana = self.object_dict["mana"]

        # Position
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.object_dict["grid_pos"][:]

        # Interface
        self.hp_font = self.game_dict["hp_font"]
        self.hp_size = self.game_dict["hp_size"]
        self.hp_color = self.game_dict["hp_color"]
        self.hp_offset = self.object_dict["hp_offset"][:]

        # Debug
        self.debug_color = self.object_dict["debug_color"]
        self.debug_pos = self.object_dict["debug_pos"]
        self.debug_dt = self.object_dict["debug_dt"]

        # Gameplay
        self.move_time = pygame.time.get_ticks()
        self.move_frequency = self.object_dict["move_frequency"]

    def init_vec(self):
        self.pos = vec(self.object_dict["pos"])
        self.pos_dt = vec(0, 0)
        self.vel = vec(0, 0)
        self.move_speed = vec(self.object_dict["move_speed"])

        self.pos_reset = vec(self.object_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0], self.object_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1])
        self.range = []

    def init_image(self):
        self.image = self.object_dict["image"]
        self.table = self.object_dict["table"]
        self.reverse = self.object_dict["reverse"]
        self.size = self.object_dict["size"]
        self.side = self.object_dict["side"]
        self.center = self.object_dict["center"]
        self.bobbing = self.object_dict["bobbing"]
        self.flip = self.object_dict["flip"]
        self.animation_time = self.object_dict["animation_time"]
        self.animation_loop = self.object_dict["animation_loop"]
        self.loop = 0

        # Image
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1], self.reverse)
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

        # Flip
        if self.flip:
            if self.table:
                for side in range(len(self.images_side)):
                    for index in range(len(self.images_side[side])):
                        self.images_side[side][index] = pygame.transform.flip(self.images_side[side][index], True, False)
                        self.image = self.images[self.index]
            else:
                self.image = pygame.transform.flip(self.image, True, False)

    def update_move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < self.grid_size[1]:
                if self.vel == (0, 0):
                    self.vel.x = self.move_speed[0] * self.range[0][0]
                    self.vel.y = self.move_speed[1] * self.range[0][1]
                if abs(self.pos_dt[0] + self.vel.x * self.game.dt) <= self.grid_dt[0] and abs(self.pos_dt[1] + self.vel.y * self.game.dt) <= self.grid_dt[1]:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt[0] += self.vel.x * self.game.dt
                    self.pos_dt[1] += self.vel.y * self.game.dt
                else:
                    self.grid_pos[0] += self.range[0][0]
                    self.grid_pos[1] += self.range[0][1]
                    self.pos.x = self.pos.x - self.pos_dt[0] + self.grid_dt[0] * self.range[0][0]
                    self.pos.y = self.pos.y - self.pos_dt[1] + self.grid_dt[1] * self.range[0][1]
                    self.pos_dt = [0, 0]
                    self.vel = vec(0, 0)
                    del self.range[0]
            else:
                del self.range[0]

        elif pygame.time.get_ticks() - self.move_time > self.move_frequency:
            dx = dy = 0
            while (dx == dy == 0 or dx != 0 and dy != 0) or not (0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]):
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
            self.range.append([dx, dy])
            self.move_time = pygame.time.get_ticks()
            self.update_move()

    def draw_ui(self):
        # Grid Pos
        pygame.draw.rect(self.game.gameDisplay, self.debug_color, (self.debug_pos[0] + self.grid_pos[0] * self.grid_dt[0], self.debug_pos[1] + self.grid_pos[1] * self.grid_dt[1], self.debug_dt[0], self.debug_dt[1]))

    def draw_debug_mode(self):
        pygame.draw.rect(self.game.gameDisplay, CYAN, (self.debug_pos[0] + self.grid_pos[0] * self.grid_dt[0], self.debug_pos[1] + self.grid_pos[1] * self.grid_dt[1], self.debug_dt[0], self.debug_dt[1]), 1)

    def draw_status(self):
        # Health
        self.game.draw_text(str(self.health), self.hp_font, self.hp_size, self.hp_color, int(self.pos[0] + self.hp_offset[0]), int(self.pos[1] + self.hp_offset[1]), "center", self.game.debug_mode)

    def update(self):
        self.game.update_sprite(self, move=True)
