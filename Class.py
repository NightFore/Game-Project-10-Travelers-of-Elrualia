import pygame

from Settings import *
from Function import *

PLACEHOLDER = 32

"""
    Others Functions
"""
class Cursor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = LAYER_CURSOR
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Position
        self.pos = [x, y]

        # Surface
        self.image = transparent_surface(PLACEHOLDER, PLACEHOLDER, YELLOW, 6)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def move(self, dx=0, dy=0):
        self.pos[0] += dx
        self.pos[1] += dy
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, name):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_PLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.name = name

        # Position
        self.pos = [int(x / TILESIZE), int(y / TILESIZE)]

        # Surface
        self.base_index = 1
        self.index = self.base_index
        self.images = image
        self.images_bottom = self.images[0]
        self.images_left = self.images[1]
        self.images_right = self.images[2]
        self.images_top = self.images[3]
        self.images = self.images_bottom
        self.image = self.images_bottom[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] * TILESIZE
        self.rect.y = self.pos[1] * TILESIZE

        self.dt = game.dt
        self.current_time = 0
        self.animation_time = 0.50

    def update(self):
        update_time_dependent(self)
        self.current_time += self.dt

        self.rect.x = self.pos[0] * TILESIZE
        self.rect.y = self.pos[1] * TILESIZE

    def attack(self):
        pass