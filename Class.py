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
        self.damage = self.object_dict["damage"]
        self.mana_cost = self.object_dict["mana_cost"]
        self.energy_cost = self.object_dict["energy_cost"]

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

        self.mana_pos = self.game_dict["mana_pos"]
        self.energy_pos = self.game_dict["energy_pos"]

    def update_move(self):
        if len(self.range) > 0:
            if 0 <= self.grid_pos[0] + self.range[0][0] < self.grid_size[0] and 0 <= self.grid_pos[1] + self.range[0][1] < self.grid_size[1]:
                update_move(self)
            else:
                del self.range[0]

    def buffer_move(self, dx=0, dy=0):
        if len(self.range) < 2 and self.energy - 1 >= 0.10:
            self.energy = max(self.energy - 1, 0)
            self.range.append([dx, dy])

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x] or keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                init_spell(Spell, self.game, self.game.spell_dict, "energy_ball", self.game.spells, self)
        if keys[pygame.K_c]:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_rate:
                init_spell(Spell, self.game, self.game.spell_dict, "thunder", self.game.spells, self)

    def draw_ui(self):
        # Cooldown
        pygame.draw.rect(self.game.gameDisplay, LIGHTGREY, (100, 620, 40, max(-40, -40 * (pygame.time.get_ticks() - self.last_attack) / self.attack_rate)))
        self.game.draw_text("X", None, 40, BLUE, (120, 600), "center", self.game.debug_mode)

        pygame.draw.rect(self.game.gameDisplay, LIGHTGREY, (270, 630, 100 * self.mana / self.max_mana, 40))
        self.game.draw_text(int(self.mana), self.ui_font, self.ui_size, self.ui_color, self.mana_pos, "center", self.game.debug_mode)
        self.game.draw_text("Mana", self.ui_font, self.ui_size, self.ui_color, (280, 635), "nw", self.game.debug_mode)

        pygame.draw.rect(self.game.gameDisplay, LIGHTGREY, (420, 630, 100 * self.energy / self.max_energy, 40))
        self.game.draw_text(int(self.energy), self.ui_font, self.ui_size, self.ui_color, self.energy_pos, "center", self.game.debug_mode)
        self.game.draw_text("Energy", self.ui_font, self.ui_size, self.ui_color, (420, 635), "nw", self.game.debug_mode)

    def draw_debug(self):
        pygame.draw.rect(self.game.gameDisplay, CYAN, (100, 620, 40, -40), 1)
        pygame.draw.rect(self.game.gameDisplay, CYAN, (100, 620, 40, max(-40, -40 * (pygame.time.get_ticks() - self.last_attack) / self.attack_rate)), 1)

    def draw_status(self):
        pass

    def update_status(self):
        self.mana = min(self.max_mana, self.mana + self.mana_regen * self.dt)
        self.energy = max(0, self.energy + self.energy_regen * self.dt)

    def update(self):
        self.game.update_sprite(self, move=True, keys=True)
        self.update_status()



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
        pass

    def draw_debug(self):
        pass

    def draw_status(self):
        pass

    def update(self):
        self.game.update_sprite(self, move=True)
