import pygame
import pytweening as tween
import random

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
    def __init__(self, game, dict, game_dict=None, character="player"):
        # Setup
        self.game = game
        self.groups = self.game.all_sprites, self.game.characters
        self._layer = LAYER_CHARACTERS
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialization
        self.dict, self.char_dict, self.game_dict = dict, dict[character], game_dict
        self.init_dict(), self.init_spell()

        # Image
        self.tile = self.table
        if self.table:
            self.index = 0
            self.images_side = load_tile_table(path.join(self.game.graphics_folder, self.image), self.size[0], self.size[1])
            self.images = self.images_side[self.side]
            self.image = self.images[self.index]
            self.dt = game.dt
            self.current_time = 0
            self.animation_time = 0.08
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

        self.level = self.char_dict["level"]
        self.max_health = self.char_dict["max_health"]
        self.health = self.char_dict["health"]
        self.max_mana = self.char_dict["max_mana"]
        self.mana = self.char_dict["mana"]

        self.grid_size = self.game_dict["grid_size"]
        self.pos_dt = self.game_dict["pos_dt"]
        self.spell_color = self.game_dict["color"]["spell"]



    def init_spell(self):
        self.waiting_spell = [None] * 9
        for index in range(len(self.waiting_spell)):
            self.waiting_spell[index] = random.choice(list(self.game.spell_images.keys()))
        self.current_spell = [None] * 3
        for index in range(len(self.current_spell)):
            self.current_spell[index] = random.choice(list(self.game.spell_images.keys()))
        self.next_spell = random.choice(list(self.game.spell_images.keys()))
        self.current_passive = random.choice(list(self.game.passive_images.keys()))

    def update_spell(self):
        for index in range(len(self.current_spell)):
            if self.current_spell[index] is None:
                self.current_spell[index] = self.next_spell = self.waiting_spell[0]
                self.waiting_spell[0] = None
                sort_list(self.waiting_spell, None)
                self.waiting_spell[len(self.waiting_spell)-1] = random.choice(list(self.game.spell_images.keys()))

    def move(self, dx=0, dy=0):
        if 0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]:
            self.pos[0] += dx * self.pos_dt[0]
            self.pos[1] += dy * self.pos_dt[1]
            self.grid_pos[0] += dx
            self.grid_pos[1] += dy
            return True
        else:
            return False

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

    def draw_ui(self):
        pass

    def update(self):
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
        self.tile = dict["tile"]
        if self.tile:
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
