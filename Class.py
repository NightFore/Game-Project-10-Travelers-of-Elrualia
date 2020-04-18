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
    def __init__(self, game, x, y, x_dt, y_dt, image, name, center=True):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_PLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.name = name

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

    def update(self):
        if self.instance_list:
            update_time_dependent(self)
            self.current_time += self.dt

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.center:
            self.rect.center = self.pos




class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type, center=True, bobbing=False):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.items
        self._layer = LAYER_ITEMS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.type = type

        # Position
        self.pos = [x, y]

        # Surface
        self.base_index = 0
        self.index = self.base_index
        self.images = self.game.item_images[self.type]
        self.instance_list = isinstance(self.images, list)

        if self.instance_list:
            self.image = self.game.item_images[self.type][self.index]
        else:
            self.image = self.game.item_images[self.type]

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