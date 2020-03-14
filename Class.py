import pygame

from Settings import *
from Function import *

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
        self.pos = [int(x / TILESIZE), int(y / TILESIZE)]

        # Surface
        self.image = transparent_surface(TILESIZE, TILESIZE, YELLOW, 6)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] * TILESIZE
        self.rect.y = self.pos[1] * TILESIZE

        # Action
        self.selection = pygame.sprite.Sprite()
        self.selection_mov = [[]]

    def move(self, dx=0, dy=0):
        if not collision(self, self.game.obstacle, dx, dy):
            if self.selection.alive():
                x_pos = self.selection.sprite.movement + self.pos[0] - self.selection.sprite.pos[0] + dx
                y_pos = self.selection.sprite.movement + self.pos[1] - self.selection.sprite.pos[1] + dy
                mov = self.selection.sprite.movement
                atk = self.selection.sprite.range

                mov_check = atk_check = False
                if 0 <= x_pos < 2*mov+1 and 0 <= y_pos < 2*mov+1:
                    mov_check = self.selection_mov[y_pos][x_pos]
                if 0 <= x_pos+atk < 2*(mov+atk)+1 and 0 <= y_pos+atk < 2*(mov+atk)+1:
                    atk_check = self.selection_atk[y_pos+atk][x_pos+atk]
                if not mov_check and not atk_check:
                    dx = dy = 0

            self.pos[0] += dx
            self.pos[1] += dy
            self.rect.x = self.pos[0] * TILESIZE
            self.rect.y = self.pos[1] * TILESIZE

    def action(self):
        if not self.selection.alive():
            for sprite in self.game.characters:
                if sprite.pos == self.pos:
                    self.selection = Selection(self.game, sprite, self.pos[0], self.pos[1], TILESIZE, TILESIZE)
                    mov = self.selection.sprite.movement
                    atk = self.selection.sprite.range
                    self.selection_mov = [[False] * (mov*2+1) for i in range(mov*2+1)]
                    self.selection_atk = [[False] * ((mov+atk)*2+1) for i in range((mov+atk)*2+1)]

                    # Selection Movement Range Grid
                    for i in range(2*mov+1):
                        for j in range(2*mov+1):
                            if abs(i-mov) + abs(j-mov) <= mov:
                                if not collision(self.selection, self.game.obstacle, j-mov, i-mov) and not collision(self.selection, self.game.characters, j-mov, i-mov):
                                    self.selection_mov[i][j] = True
                    self.selection_mov[mov][mov] = True
                    reachable(self.selection_mov, mov, mov, 1)

                    # Selection Attack Range Grid
                    for i in range(2*mov+1):
                        for j in range(2*mov+1):
                            if self.selection_mov[i][j]:
                                for x in range(-atk, atk+1):
                                    for y in range(-atk, atk+1):
                                        if abs(x) + abs(y) == atk:
                                            if not collision(self.selection, self.game.obstacle, j-mov+y, i-mov+x):
                                                if 0 <= i+x < 2*mov+1 and 0 <= j+y < 2*mov+1:
                                                    if not self.selection_mov[i+x][j+y]:
                                                        self.selection_atk[i+x+atk][j+y+atk] = True
                                                else:
                                                    self.selection_atk[i+x+atk][j+y+atk] = True
        else:
            self.selection.sprite.pos[0] = self.pos[0]
            self.selection.sprite.pos[1] = self.pos[1]
            self.selection.kill()

    def update(self):
        pass



class Selection(pygame.sprite.Sprite):
    def __init__(self, game, sprite, x, y, w, h):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = LAYER_SELECTION
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Settings
        self.sprite = sprite

        # Surface
        self.image = pygame.Surface((TILESIZE, TILESIZE)).convert()
        self.image.fill(BLUE)

        # Position
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.x = self.pos[0]*w
        self.rect.y = self.pos[1]*h



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        # Setup
        self.game = game
        self.groups = self.game.obstacle
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Position
        self.rect = pygame.Rect(x, y, w, h)
        self.pos = [x, y]
        self.rect.x = self.pos[0]*w
        self.rect.y = self.pos[1]*h



class Weapon:
    def __init__(self, attack, hit, critical, range, weight):
        self.attack = attack
        self.hit = hit
        self.critical = critical
        self.range = range
        self.weight = weight

class Iron_Sword(Weapon):
    def __init__(self):
        Weapon.__init__(self, 5, 100, 0, 1, 2)

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