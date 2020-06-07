import pygame
import pytweening as tween

from Settings import *
from Function import *


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




class Player(pygame.sprite.Sprite):
    def __init__(self, game, dict, ui_dict=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.dict = dict
        self.ui_dict = ui_dict
        self.init_dict()
        self.init_spell()

        # Settings
        self.name = self.dict["name"]
        self.pos = self.dict["pos"]
        self.pos_dt = self.dict["pos_dt"]

        # Image
        self.tile = dict["tile"]
        if self.tile:
            image = load_tile_table(path.join(self.game.graphics_folder, self.dict["image"]), self.dict["tile_dt"][0], self.dict["tile_dt"][1])
            self.index = 0
            self.images_bottom = image[0]
            self.images_left = image[1]
            self.images_right = image[2]
            self.images_top = image[3]
            self.images = self.images_right
            self.image = self.images[self.index]
            self.dt = game.dt
            self.current_time = 0
            self.animation_time = 0.50
        else:
            self.image = load_image(self.game.graphics_folder, self.dict["image"])
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = dict["center"]
        if self.center:
            self.rect.center = self.pos

        # Bobbing
        self.bobbing = dict["bobbing"]
        self.tween = tween.linear
        self.step = 0
        self.dir = 1

    def init_dict(self):
        self.grid_pos = self.dict["grid_pos"]
        self.grid_size = self.ui_dict["grid_size"]

        self.max_health = self.dict["max_health"]
        self.health = self.dict["health"]
        self.health_rect = self.dict["health_rect"]
        self.health_color = self.ui_dict["health"]

        self.max_armor = self.dict["max_armor"]
        self.armor = self.dict["armor"]
        self.armor_rect = self.dict["armor_rect"]
        self.armor_color = self.ui_dict["armor"]

        self.max_mana = self.dict["max_mana"]
        self.mana = self.dict["mana"]
        self.mana_rect = self.dict["mana_rect"]
        self.mana_dt = self.dict["mana_dt"]
        self.mana_color = self.ui_dict["mana"]

        self.c_spell_pos = self.dict["current_spell_pos"]
        self.c_spell_dt = self.dict["current_spell_dt"]
        self.w_spell_pos = self.dict["waiting_spell_pos"]
        self.w_spell_dt = self.dict["waiting_spell_dt"]
        self.n_spell_pos = self.dict["next_spell_pos"]
        self.p_spell_pos = self.dict["passive_spell_pos"]
        self.color_spell = self.ui_dict["spell_color"]
        self.color_spell_pos = self.ui_dict["spell_color_pos"]
        self.color_spell_dt = self.ui_dict["spell_color_dt"]
        self.spell_size = self.ui_dict["spell_size"]
        self.spell_dt = self.ui_dict["spell_dt"]
        self.spell_side_dt = self.ui_dict["spell_side_dt"]

    def init_spell(self):
        self.waiting_spell = [None] * 9
        for index in range(len(self.waiting_spell)):
            self.waiting_spell[index] = random.choice(list(self.game.spell_images.keys()))
        self.current_spell = [None] * 3
        for index in range(len(self.current_spell)):
            self.current_spell[index] = random.choice(list(self.game.spell_images.keys()))
        self.next_spell = random.choice(list(self.game.spell_images.keys()))
        self.current_passive = random.choice(list(self.game.passive_images.keys()))

    def move(self, dx=0, dy=0):
        if 0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]:
            self.pos[0] += dx * self.pos_dt[0]
            self.pos[1] += dy * self.pos_dt[1]
            self.grid_pos[0] += dx
            self.grid_pos[1] += dy

    def draw_status(self):
        # Health / Armor / Mana
        pygame.draw.rect(self.game.gameDisplay, self.health_color, (self.health_rect[0], self.health_rect[1], self.health/self.max_health * self.health_rect[2], self.health_rect[3]))
        pygame.draw.rect(self.game.gameDisplay, self.armor_color, (self.armor_rect[0], self.armor_rect[1], self.armor/self.max_armor * self.armor_rect[2], self.armor_rect[3]))
        for i in range(int(self.mana)+1):
            pygame.draw.rect(self.game.gameDisplay, self.mana_color, (self.mana_rect[0] + i*self.mana_dt[0], self.mana_rect[1] + i*self.mana_dt[1], min(1, self.mana-i) * self.mana_rect[2], self.mana_rect[3]))

    def draw_spell(self):
        # Current Spell & Colors
        for i in range(len(self.current_spell)):
            pygame.draw.rect(self.game.gameDisplay, self.color_spell[i], (self.color_spell_pos[0] + i*self.color_spell_dt[0], self.color_spell_pos[1] + i*self.color_spell_dt[1], self.color_spell_pos[2], self.color_spell_pos[3]))
            if self.current_spell[i] is not None:
                self.game.draw_image(self.game.spell_images[self.current_spell[i]], self.c_spell_pos[0] + i*self.c_spell_dt[0], self.c_spell_pos[1] + i*self.c_spell_dt[1])

        # Waiting Spell
        for i in range(len(self.waiting_spell)):
            if self.waiting_spell[i] is not None:
                if i == 0:
                    self.game.draw_image(self.game.spell_images[self.waiting_spell[i]], self.n_spell_pos[0], self.n_spell_pos[1])
                else:
                    self.game.draw_image(self.game.spell_images[self.waiting_spell[i]], self.w_spell_pos[0] + i*self.w_spell_dt[0], self.w_spell_pos[1] + i*self.w_spell_dt[1])

        # Current Passive
        self.game.draw_image(self.game.passive_images[self.current_passive], self.p_spell_pos[0], self.p_spell_pos[1])

    def draw_spell_range(self):
        for index in range(len(self.current_spell)):
            spell = self.current_spell[index]

            if SPELL_DICT[spell]["type"] == 0:
                pygame.draw.circle(self.game.gameDisplay, self.color_spell[index], (self.pos[0], self.pos[1]), self.spell_size)

            if SPELL_DICT[spell]["type"] == 1:
                for h in range(len(SPELL_DICT[spell]["range"])):
                    for v in range(len(SPELL_DICT[spell]["range"][h])):
                        grid_pos_x = self.grid_pos[0] + h + 1 - self.grid_size[0]
                        grid_pos_y = self.grid_pos[1] + (v-int(len(SPELL_DICT[spell]["range"][h])/2))
                        if 0 <= grid_pos_x < self.grid_size[0] and 0 <= grid_pos_y < self.grid_size[1]:
                            pos_x = self.pos[0] + h*self.spell_dt + self.spell_side_dt
                            pos_y = self.pos[1] + (v-int(len(SPELL_DICT[spell]["range"][h])/2))*self.spell_dt
                            pygame.draw.circle(self.game.gameDisplay, self.color_spell[index], (pos_x, pos_y), self.spell_size)

    def use_spell(self, index):
        spell = self.current_spell[index]
        if SPELL_DICT[spell]["type"] == 1:
            hit = False
            for h in range(len(SPELL_DICT[spell]["range"])):
                for v in range(len(SPELL_DICT[spell]["range"][h])):
                    grid_pos_x = self.grid_pos[0] + h + 1 - self.grid_size[0]
                    grid_pos_y = self.grid_pos[1] + (v-int(len(SPELL_DICT[spell]["range"][h])/2))
                    if grid_pos_x == self.game.enemy.grid_pos[0] and grid_pos_y == self.game.enemy.grid_pos[1]:
                        hit = True
            if hit:
                self.game.enemy.health = max(0, self.game.enemy.health - SPELL_DICT[spell]["damage"])

        self.current_spell[index] = None
        self.update_spell()

    def update_spell(self):
        for index in range(len(self.current_spell)):
            if self.current_spell[index] is None:
                self.current_spell[index] = self.next_spell = self.waiting_spell[0]
                self.waiting_spell[0] = None
                sort_list(self.waiting_spell, None)
                self.waiting_spell[len(self.waiting_spell)-1] = random.choice(list(self.game.spell_images.keys()))

    def draw_ui(self):
        self.draw_status()
        self.draw_spell()
        self.draw_spell_range()

    def update(self):
        self.game.update_sprite(self)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, dict, ui_dict=None):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.dict = dict
        self.ui_dict = ui_dict
        self.init_dict()

        # Settings
        self.name = self.dict["name"]
        self.pos = self.dict["pos"]
        self.pos_dt = self.dict["pos_dt"]

        # Image
        self.tile = dict["tile"]
        if self.tile:
            image = load_tile_table(path.join(self.game.graphics_folder, self.dict["image"]), self.dict["tile_dt"][0], self.dict["tile_dt"][1])
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
            self.image = load_image(self.game.graphics_folder, self.dict["image"])
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = dict["center"]
        if self.center:
            self.rect.center = self.pos

        # Bobbing
        self.bobbing = dict["bobbing"]
        self.tween = tween.linear
        self.step = 0
        self.dir = 1

    def init_dict(self):
        self.grid_pos = self.dict["grid_pos"]
        self.grid_size = self.ui_dict["grid_size"]

        self.max_health = self.dict["max_health"]
        self.health = self.dict["health"]
        self.health_rect = self.dict["health_rect"]
        self.health_color = self.ui_dict["health"]

        self.max_mana = self.dict["max_mana"]
        self.mana = self.dict["mana"]
        self.mana_rect = self.dict["mana_rect"]
        self.mana_dt = self.dict["mana_dt"]
        self.mana_color = self.ui_dict["mana"]

    def move(self, dx=0, dy=0):
        if 0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]:
            self.pos[0] += dx * self.pos_dt[0]
            self.pos[1] += dy * self.pos_dt[1]
            self.grid_pos[0] += dx
            self.grid_pos[1] += dy

    def draw_status(self):
        # Health / Mana
        pygame.draw.rect(self.game.gameDisplay, self.health_color, (self.health_rect[0], self.health_rect[1] + (1 - self.health / self.max_health) * self.health_rect[3], self.health_rect[2], self.health/self.max_health * self.health_rect[3]))
        for i in range(int(self.mana)+1):
            pygame.draw.rect(self.game.gameDisplay, self.mana_color, (self.mana_rect[0] + i*self.mana_dt[0], self.mana_rect[1] + i*self.mana_dt[1] + (1-min(1, self.mana-i))*self.mana_rect[3], self.mana_rect[2], min(1, self.mana-i) * self.mana_rect[3]))

    def draw_ui(self):
        self.draw_status()

    def update(self):
        self.game.update_sprite(self)




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
        self.tile = isinstance(self.images, list)

        if self.tile:
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
