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
    max_health = 100
    max_armor = 50
    max_mana = 5
    health = max_health
    armor = max_armor/2
    mana = 3.75

    waiting_spell = [None] * 9
    current_spell = [None] * 3
    current_passive = [None]

    def update_spell(self):
        if None in self.current_spell:
            sort_list(self.current_spell, None)
            for index in range(len(self.current_spell)):
                if self.current_spell[index] is None:
                    self.current_spell[index] = self.waiting_spell[index]
                    self.waiting_spell[index] = None

        if None in self.waiting_spell:
            sort_list(self.waiting_spell, None)
            for index in range(len(self.waiting_spell)):
                if self.waiting_spell[index] is None:
                    self.waiting_spell[index] = random.choice(list(self.game.spell_images.keys()))

        if None in self.current_passive:
            self.current_passive[0] = random.choice(list(self.game.passive_images.keys()))

    def __init__(self, game, x, y, x_dt, y_dt, image, name, center=True):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_PLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.name = name
        self.update_spell()

        # Position
        self.pos = [x, y]
        self.pos_dt = [x_dt, y_dt]

        # Surface
        self.base_index = 0
        self.index = self.base_index
        self.instance_list = isinstance(image, list)

        if self.instance_list:
            self.images = self.game.player_img
            self.images_bottom = self.images[0]
            self.images_left = self.images[1]
            self.images_right = self.images[2]
            self.images_top = self.images[3]
            self.images = self.images_bottom
            self.image = self.images_bottom[self.index]
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

        # Time
        self.dt = game.dt
        self.current_time = 0
        self.animation_time = 0.50

    def move(self, dx=0, dy=0):
        self.pos[0] += dx * self.pos_dt[0]
        self.pos[1] += dy * self.pos_dt[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw_status(self):
        pygame.draw.rect(self.game.gameDisplay, HEALTH_COLOR, (PLAYER_HEALTH_X, PLAYER_HEALTH_Y, self.health/self.max_health * PLAYER_HEALTH_WIDTH, PLAYER_HEALTH_HEIGHT))
        pygame.draw.rect(self.game.gameDisplay, ARMOR_COLOR, (PLAYER_ARMOR_X, PLAYER_ARMOR_Y, self.armor/self.max_armor * PLAYER_ARMOR_WIDTH, PLAYER_ARMOR_HEIGHT))

        for i in range(self.max_mana):
            if self.mana-i >= 0:
                pygame.draw.rect(self.game.gameDisplay, MANA_COLOR, (PLAYER_MANA_X + i*MANA_X_DT, PLAYER_MANA_Y, min(1, self.mana-i) * MANA_WIDTH, MANA_HEIGHT))

    def update(self):
        self.update_spell()

        if self.instance_list:
            update_time_dependent(self)
            self.current_time += self.dt

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.center:
            self.rect.center = self.pos




class Enemy(pygame.sprite.Sprite):
    max_health = 100
    max_armor = 50
    max_mana = 3
    health = max_health
    armor = max_armor/2
    mana = 1.50

    def __init__(self, game,  x, y, image, name, center=True):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_PLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.name = name

        # Position
        self.pos = [x, y]

        # Surface
        self.image = image

        # Rect
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # Center
        self.center = center
        if self.center:
            self.rect.center = self.pos

    def draw_status(self):
        pygame.draw.rect(self.game.gameDisplay, HEALTH_COLOR, (ENEMY_HEALTH_X, ENEMY_HEALTH_Y, self.health/self.max_health * ENEMY_HEALTH_WIDTH, ENEMY_HEALTH_HEIGHT))

        for i in range(self.max_mana):
            if self.mana-i >= 1:
                pygame.draw.rect(self.game.gameDisplay, MANA_COLOR, (ENEMY_MANA_X, ENEMY_MANA_Y + i*MANA_Y_DT, MANA_WIDTH, MANA_HEIGHT))

            elif self.mana-i > 0:
                pygame.draw.rect(self.game.gameDisplay, MANA_COLOR, (ENEMY_MANA_X, ENEMY_MANA_Y + i*MANA_Y_DT + int(0.5+(1-(self.mana-i))*MANA_HEIGHT), MANA_WIDTH, int(0.5+(self.mana-i)*MANA_HEIGHT)))

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.center:
            self.rect.center = self.pos




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
        self.base_index = 0
        self.index = self.base_index
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
        if self.bobbing:
            update_bobbing(self)

        if self.instance_list:
            update_time_dependent(self)
            self.current_time += self.dt

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.center:
            self.rect.center = self.pos