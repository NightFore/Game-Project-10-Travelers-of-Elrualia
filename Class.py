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
    grid_pos = [0, 0]

    max_health = 100
    max_armor = 50
    max_mana = 5
    health = max_health
    armor = max_armor/2
    mana = 3.75

    waiting_spell = [None] * 9
    current_spell = [None] * 3
    current_passive = None

    def __init__(self, game, x, y, x_dt, y_dt, image, name, center=True, bobbing=False):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.name = name
        self.update_spell()

        # Position
        self.pos = [x, y]
        self.pos_dt = [x_dt, y_dt]

        # Surface
        self.index = 0
        self.instance_list = isinstance(image, list)

        if self.instance_list:
            self.images = self.game.player_img
            self.images_bottom = self.images[0]
            self.images_left = self.images[1]
            self.images_right = self.images[2]
            self.images_top = self.images[3]
            self.images = self.images_right
            self.image = self.images[self.index]
            self.dt = game.dt
            self.current_time = 0
            self.animation_time = 0.50
        else:
            self.image = image

        # Rect
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = center
        if self.center:
            self.rect.center = self.pos

        # Bobbing
        self.bobbing = bobbing
        self.tween = tween.linear
        self.step = 0
        self.dir = 1

    def move(self, dx=0, dy=0):
        if 0 <= self.grid_pos[0] + dx < 4 and 0 <= self.grid_pos[1] + dy < 4:
            self.pos[0] += dx * self.pos_dt[0]
            self.pos[1] += dy * self.pos_dt[1]
            self.grid_pos[0] += dx
            self.grid_pos[1] += dy

    def draw_status(self):
        # Health / Armor / Mana
        pygame.draw.rect(self.game.gameDisplay, HEALTH_COLOR, (PLAYER_HEALTH_X, PLAYER_HEALTH_Y, self.health/self.max_health * PLAYER_HEALTH_WIDTH, PLAYER_HEALTH_HEIGHT))
        pygame.draw.rect(self.game.gameDisplay, ARMOR_COLOR, (PLAYER_ARMOR_X, PLAYER_ARMOR_Y, self.armor/self.max_armor * PLAYER_ARMOR_WIDTH, PLAYER_ARMOR_HEIGHT))
        for i in range(int(self.mana)+1):
            pygame.draw.rect(self.game.gameDisplay, MANA_COLOR, (PLAYER_MANA_X + i*MANA_X_DT, PLAYER_MANA_Y, min(1, self.mana-i) * MANA_WIDTH, MANA_HEIGHT))

    def draw_spell(self):
        # Current Spell & Colors
        for i in range(len(self.current_spell)):
            pygame.draw.rect(self.game.gameDisplay, COLOR_SPELL[i], (203 + 60*i, 643, 54, 54))
            if self.current_spell[i] is not None:
                self.game.draw_image(self.game.spell_images[self.current_spell[i]], 230 + 60*i, 670)

        # Waiting Spell
        for i in range(len(self.waiting_spell)):
            if self.waiting_spell[i] is not None:
                if i == 0:
                    self.game.draw_image(self.game.spell_images[self.waiting_spell[i]], 130, 670)
                else:
                    self.game.draw_image(self.game.spell_images[self.waiting_spell[i]], 70, 730-60*i)

        # Current Passive
        self.game.draw_image(self.game.passive_images[self.current_passive], 410, 670)

    def draw_spell_range(self):
        for index in range(len(self.current_spell)):
            spell = self.current_spell[index]

            if SPELL_DICT[spell]["type"] == 0:
                pygame.draw.circle(self.game.gameDisplay, COLOR_SPELL[index], (self.pos[0], self.pos[1]), 38)

            if SPELL_DICT[spell]["type"] == 1:
                for h in range(len(SPELL_DICT[spell]["range"])):
                    for v in range(len(SPELL_DICT[spell]["range"][h])):
                        if SPELL_DICT[spell]["range"][h][v]:
                            pos_x = self.pos[0] + h*SPELL_DT + GRID_SIDE_DT
                            pos_y = self.pos[1] + (v-int(len(SPELL_DICT[spell]["range"][h])/2))*SPELL_DT
                            pygame.draw.circle(self.game.gameDisplay, COLOR_SPELL[index], (pos_x, pos_y), 38)

    def update_spell(self):
        while None in self.waiting_spell or None in self.current_spell:
            sort_list(self.waiting_spell, None)
            for index in range(len(self.waiting_spell)):
                if self.waiting_spell[index] is None:
                    self.waiting_spell[index] = random.choice(list(self.game.spell_images.keys()))

            index_w = 0
            for index in range(len(self.current_spell)):
                if self.current_spell[index] is None:
                    if self.waiting_spell[index_w] is not None:
                        self.current_spell[index] = self.waiting_spell[index_w]
                        self.waiting_spell[index_w] = None
                    index_w += 1

        if self.current_passive is None:
            self.current_passive = random.choice(list(self.game.passive_images.keys()))

    def update(self):
        self.game.draw_sprite(self)




class Enemy(pygame.sprite.Sprite):
    max_health = 100
    max_armor = 50
    max_mana = 3
    health = max_health
    armor = max_armor/2
    mana = 4.50

    def __init__(self, game, x, y, x_dt, y_dt, image, name, center=True, bobbing=False):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.name = name

        # Position
        self.pos = [x, y]
        self.pos_dt = [x_dt, y_dt]

        # Surface
        self.index = 0
        self.instance_list = isinstance(image, list)

        if self.instance_list:
            self.images = self.game.player_img
            self.images_bottom = self.images[0]
            self.images_left = self.images[1]
            self.images_right = self.images[2]
            self.images_top = self.images[3]
            self.images = self.images_right
            self.image = self.images[self.index]
            self.dt = game.dt
            self.current_time = 0
            self.animation_time = 0.50
        else:
            self.image = image

        # Rect
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = center
        if self.center:
            self.rect.center = self.pos

        # Bobbing
        self.bobbing = bobbing
        self.tween = tween.linear
        self.step = 0
        self.dir = 1

    def draw_status(self):
        # Health / Mana
        pygame.draw.rect(self.game.gameDisplay, HEALTH_COLOR, (ENEMY_HEALTH_X, ENEMY_HEALTH_Y, self.health/self.max_health * ENEMY_HEALTH_WIDTH, ENEMY_HEALTH_HEIGHT))
        for i in range(int(self.mana)+1):
            pygame.draw.rect(self.game.gameDisplay, MANA_COLOR, (ENEMY_MANA_X, ENEMY_MANA_Y + i*MANA_Y_DT + (1-min(1, self.mana-i))*MANA_HEIGHT, MANA_WIDTH, min(1, self.mana-i) * MANA_HEIGHT))

    def update(self):
        self.game.draw_sprite(self)




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
        self.instance_list = isinstance(self.images, list)

        if self.instance_list:
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
        self.game.draw_sprite(self)
