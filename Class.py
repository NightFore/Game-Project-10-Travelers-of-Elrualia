import pygame
import pytweening as tween
import random

from Settings import *
from Function import *
vec = pygame.math.Vector2

"""
    Others Functions
"""
class Spell(pygame.sprite.Sprite):
    def __init__(self, game, dict, object=None, group=None, parent=None):
        init_sprite(self, game, dict, object, group, parent)

    def init_settings(self):
        # Position
        self.grid_size = self.game_dict["grid_size"]
        self.grid_pos = vec(self.parent.grid_pos[:])
        self.grid_dt = vec(self.game_dict["grid_dt"])
        offset = [self.parent.object_dict["spell_offset"][0] + self.parent.object_dict["cast_offset"][0] + self.parent.pos_dt[0],
                  self.parent.object_dict["spell_offset"][1] + self.parent.object_dict["cast_offset"][1]]
        self.pos += self.grid_pos[0] * self.grid_dt[0] + offset[0], self.grid_pos[1] * self.grid_dt[1] + offset[1]
        if self.move:
            self.pos_dt = vec(offset[0], 0)

        # Gameplay
        self.spawn_time = pygame.time.get_ticks()
        self.parent.last_attack = self.spawn_time
        self.damage = self.object_dict["damage"]

    def update_move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < 2 * self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < 2 * self.grid_size[1]:
                update_move(self)
            else:
                self.kill()
        else:
            self.kill()

    def collide_sprite(self):
        for sprite in self.game.characters:
            if sprite != self.parent and (self.grid_pos[0] - self.grid_size[0] == sprite.grid_pos[0] and self.grid_pos[1] == sprite.grid_pos[1]):
                sprite.health -= self.damage
                if self.impact:
                    Impact(self.game, self.dict, self.object + "_impact", self.group, self)
                self.kill()

    def update(self):
        self.game.update_sprite(self, move=self.move)
        self.collide_sprite()
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()


class Impact(pygame.sprite.Sprite):
    def __init__(self, game, dict, object=None, group=None, parent=None):
        init_sprite(self, game, dict, object, group, parent)

    def init_settings(self):
        # Position
        self.grid_size = self.game_dict["grid_size"]
        self.grid_pos = vec(self.parent.grid_pos[:])
        self.grid_dt = vec(self.game_dict["grid_dt"])
        self.pos = self.parent.pos

        # Gameplay
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.game.update_sprite(self)



class Player(pygame.sprite.Sprite):
    def __init__(self, game, dict, object=None, group=None, parent=None):
        init_sprite(self, game, dict, object, group, parent)

    def init_settings(self):
        init_character(self), init_interface(self)

        # Gameplay
        self.last_attack = pygame.time.get_ticks()
        self.attack_rate = self.object_dict["attack_rate"]

    def update_move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < self.grid_size[1]:
                update_move(self)
            else:
                del self.range[0]

    def buffer_move(self, dx=0, dy=0):
        if len(self.range) < 2:
            self.range.append([dx, dy])

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x] or keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                Spell(self.game, self.game.spell_dict, "energy_ball", self.game.spells, self)
        if keys[pygame.K_c]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                Spell(self.game, self.game.spell_dict, "thunder", self.game.spells, self)

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
    def __init__(self, game, dict, object=None, group=None, parent=None):
        init_sprite(self, game, dict, object, group, parent)

    def init_settings(self):
        init_character(self), init_interface(self)

        # Gameplay
        self.last_move = pygame.time.get_ticks()
        self.move_frequency = self.object_dict["move_frequency"]

    def update_move(self):
        if len(self.range) == 0 and pygame.time.get_ticks() - self.last_move > self.move_frequency:
            dx = dy = 0
            while (dx == dy == 0 or dx != 0 and dy != 0) or not (0 <= self.grid_pos[0] + dx < self.grid_size[0] and 0 <= self.grid_pos[1] + dy < self.grid_size[1]):
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
            self.range.append([dx, dy])
            self.last_move = pygame.time.get_ticks()

        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < self.grid_size[1]:
                update_move(self)
            else:
                del self.range[0]

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
