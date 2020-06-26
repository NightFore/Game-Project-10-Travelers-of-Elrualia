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

    def init_vec(self):
        self.offset = self.dict["offset"]
        self.cast_offset = self.dict["cast_offset"]
        character_offset = 0
        if self.character.pos_dt[0] != 0:
            character_offset = self.grid_dt[0] * self.character.pos_buffer[0][0] - self.character.pos_dt[0]
        self.pos = vec(self.game_dict["pos"]["player"][0] + self.grid_pos[0] * self.grid_dt[0] + self.offset[0] + self.cast_offset[0] + character_offset,
                       self.game_dict["pos"]["player"][1] + self.grid_pos[1] * self.grid_dt[1] + self.offset[1] + self.cast_offset[1])
        self.pos_buffer = self.object_dict["range"][:]
        self.pos_dt = vec(0, 0)
        self.vel = vec(0, 0)
        self.movespeed = vec(self.object_dict["movespeed"])

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
        if len(self.pos_buffer) > 0:
            if 0 <= self.grid_pos[0] + self.pos_buffer[0][0] < 2 * self.grid_size[0] and 0 <= self.grid_pos[1] + self.pos_buffer[0][1] < 2 * self.grid_size[1]:
                if self.vel == (0, 0):
                    self.pos_dt[0] = self.game_dict["pos"]["player"][0] + (self.grid_pos[0] + self.pos_buffer[0][0]) * self.grid_dt[0] - self.pos[0]
                    self.pos_dt[1] = self.game_dict["pos"]["player"][1] + (self.grid_pos[1] + self.pos_buffer[0][1]) * self.grid_dt[1] - self.pos[1]
                    self.vel.x = self.pos_buffer[0][0] * self.movespeed[0]
                    self.vel.y = self.pos_buffer[0][1] * self.movespeed[1]

                if self.pos_buffer[0][0] * self.pos_dt[0] > 0 or self.pos_buffer[0][1] * self.pos_dt[1] > 0:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt -= self.vel * self.game.dt
                else:
                    self.grid_pos[0] += self.pos_buffer[0][0]
                    self.grid_pos[1] += self.pos_buffer[0][1]
                    self.pos[0] = self.game_dict["pos"]["player"][0] + self.grid_pos[0] * self.grid_dt[0] + self.offset[0]
                    self.pos[1] = self.game_dict["pos"]["player"][1] + self.grid_pos[1] * self.grid_dt[1] + self.offset[1]
                    self.pos_dt = vec(0, 0)
                    self.vel = vec(0, 0)
                    del self.pos_buffer[0]
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
    def __init__(self, game, dict, game_dict=None, object="player"):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.init_dict(dict, game_dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

    def init_dict(self, dict, game_dict, object):
        self.dict = dict
        self.game_dict = game_dict
        self.object_dict = self.dict[object]

    def init_settings(self):
        # Status
        self.name = self.object_dict["name"]
        self.level = self.object_dict["level"]
        self.max_health = self.object_dict["max_health"]
        self.health = self.object_dict["health"]
        self.max_mana = self.object_dict["max_mana"]
        self.mana = self.object_dict["mana"]

        # Movement
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.object_dict["grid_pos"][:]

        # Gameplay
        self.last_attack = pygame.time.get_ticks()
        self.attack_rate = self.object_dict["attack_rate"]

    def init_vec(self):
        self.pos = vec(self.object_dict["pos"])
        self.pos_dt = vec(0, 0)
        self.vel = vec(0, 0)
        self.movespeed = vec(self.object_dict["speed"])

        self.pos_reset = vec(self.object_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0], self.object_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1])
        self.pos_buffer = []

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
        if len(self.pos_buffer) > 0:
            if 0 <= self.grid_pos[0] + self.pos_buffer[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.pos_buffer[0][1] < self.grid_size[1]:
                if self.vel == (0, 0):
                    self.pos_dt[0] = self.pos_buffer[0][0] * self.grid_dt[0]
                    self.pos_dt[1] = self.pos_buffer[0][1] * self.grid_dt[1]
                    self.vel.x = self.pos_buffer[0][0] * self.movespeed[0]
                    self.vel.y = self.pos_buffer[0][1] * self.movespeed[1]

                if self.pos_buffer[0][0] * self.pos_dt[0] > 0 or self.pos_buffer[0][1] * self.pos_dt[1] > 0:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt -= self.vel * self.game.dt
                else:
                    self.grid_pos[0] += self.pos_buffer[0][0]
                    self.grid_pos[1] += self.pos_buffer[0][1]
                    self.pos.x = self.object_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0]
                    self.pos.y = self.object_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1]
                    self.pos_dt = vec(0, 0)
                    self.vel = vec(0, 0)
                    del self.pos_buffer[0]
            else:
                del self.pos_buffer[0]

    def buffer_move(self, dx=0, dy=0):
        if len(self.pos_buffer) < 3:
            self.pos_buffer.append([dx, dy])

    def draw_debug_move(self):
        pos_x = 165 + self.grid_pos[0] * self.grid_dt[0]
        pos_y = 330 + self.grid_pos[1] * self.grid_dt[1]
        pygame.draw.rect(self.game.gameDisplay, RED, (pos_x, pos_y, 110, 60))

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x] or keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                Spell(self.game, SPELL_DICT, self.game_dict, "energy_ball", self)
                self.last_attack = pygame.time.get_ticks()

    def draw_ui(self):
        pass

    def update(self):
        self.game.update_sprite(self, move=True, keys=True)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, dict, game_dict=None, object="player"):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = dict["layer"]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.init_dict(dict, game_dict, object), self.init_settings(), self.init_vec(), self.init_image()
        self.dt = game.dt

    def init_dict(self, dict, game_dict, object):
        self.dict = dict
        self.game_dict = game_dict
        self.object_dict = self.dict[object]

    def init_settings(self):
        # Status
        self.name = self.object_dict["name"]
        self.level = self.object_dict["level"]
        self.max_health = self.object_dict["max_health"]
        self.health = self.object_dict["health"]
        self.max_mana = self.object_dict["max_mana"]
        self.mana = self.object_dict["mana"]

        # Movement
        self.grid_size = self.game_dict["grid_size"]
        self.grid_dt = self.game_dict["grid_dt"]
        self.grid_pos = self.object_dict["grid_pos"][:]

        # Gameplay
        self.move_time = pygame.time.get_ticks()
        self.move_frequency = self.object_dict["move_frequency"]

    def init_vec(self):
        self.pos = vec(self.object_dict["pos"])
        self.pos_dt = vec(0, 0)
        self.vel = vec(0, 0)
        self.movespeed = vec(self.object_dict["speed"])

        self.pos_reset = vec(self.object_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0],
                             self.object_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1])
        self.pos_buffer = []

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
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0],
                                               self.size[1])
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
        if len(self.pos_buffer) > 0:
            if 0 <= self.grid_pos[0] + self.pos_buffer[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.pos_buffer[0][1] < self.grid_size[1]:
                if self.vel == (0, 0):
                    self.pos_dt[0] = self.pos_buffer[0][0] * self.grid_dt[0]
                    self.pos_dt[1] = self.pos_buffer[0][1] * self.grid_dt[1]
                    self.vel.x = self.pos_buffer[0][0] * self.movespeed[0]
                    self.vel.y = self.pos_buffer[0][1] * self.movespeed[1]

                if self.pos_buffer[0][0] * self.pos_dt[0] > 0 or self.pos_buffer[0][1] * self.pos_dt[1] > 0:
                    self.pos += self.vel * self.game.dt
                    self.pos_dt -= self.vel * self.game.dt
                else:
                    self.grid_pos[0] += self.pos_buffer[0][0]
                    self.grid_pos[1] += self.pos_buffer[0][1]
                    self.pos.x = self.object_dict["pos"][0] + self.grid_pos[0] * self.grid_dt[0]
                    self.pos.y = self.object_dict["pos"][1] + self.grid_pos[1] * self.grid_dt[1]
                    self.pos_dt = vec(0, 0)
                    self.vel = vec(0, 0)
                    del self.pos_buffer[0]
            else:
                del self.pos_buffer[0]

        elif pygame.time.get_ticks() - self.move_time > self.move_frequency:
            dx = dy = 0
            while (dx == dy == 0 or dx != 0 and dy != 0) or not (0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]):
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
            self.pos_buffer.append([dx, dy])
            self.move_time = pygame.time.get_ticks()
            self.move()

    def draw_debug_move(self):
        pos_x = 165 + self.grid_pos[0] * self.grid_dt[0]
        pos_y = 330 + self.grid_pos[1] * self.grid_dt[1]
        pygame.draw.rect(self.game.gameDisplay, RED, (pos_x, pos_y, 110, 60))

    def draw_ui(self):
        pass

    def update(self):
        self.game.update_sprite(self, move=True)




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
