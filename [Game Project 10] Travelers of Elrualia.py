import pygame
import os
from pygame.locals import *
from os import path

from Settings import *
from ScaledGame import *
from Camera import *
from Function import *
from Class import *

vec = pygame.math.Vector2


"""
    Game
"""
class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        pygame.key.set_repeat(50, 150)
        self.gameDisplay = ScaledGame(project_title, screen_size, FPS)
        self.dt = self.gameDisplay.clock.tick(FPS) / 1000
        self.load_data()
        self.new()

    def update_sprite(self, sprite, move=False, keys=False):
        if move:
            sprite.update_move()
        if keys:
            sprite.get_keys()
        update_time_dependent(sprite)
        update_center(sprite)
        update_bobbing(sprite)

    def draw_text(self, text, font, color, pos, align="nw", debug_mode=False):
        if not isinstance(text, str):
            text = str(text)
        x, y = int(pos[0]), int(pos[1])
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        if debug_mode:
            pygame.draw.rect(self.gameDisplay, CYAN, text_rect, 1)
        self.gameDisplay.blit(text_surface, text_rect)

    def draw_image(self, image, x, y, align="center"):
        image_rect = image.get_rect()
        if align == "nw":
            image_rect.topleft = (x, y)
        if align == "ne":
            image_rect.topright = (x, y)
        if align == "sw":
            image_rect.bottomleft = (x, y)
        if align == "se":
            image_rect.bottomright = (x, y)
        if align == "n":
            image_rect.midtop = (x, y)
        if align == "s":
            image_rect.midbottom = (x, y)
        if align == "e":
            image_rect.midright = (x, y)
        if align == "w":
            image_rect.midleft = (x, y)
        if align == "center":
            image_rect.center = (x, y)
        self.gameDisplay.blit(image, image_rect)

    def load_data(self):
        # Directories
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.graphics_folder = path.join(self.data_folder, "graphics")
        self.sfx_folder = path.join(self.data_folder, "sfx")
        self.voice_folder = path.join(self.data_folder, "voice")
        self.music_folder = path.join(self.data_folder, "music")
        self.map_folder = path.join(self.data_folder, "map")

        # Dict
        self.game_dict = GAME_DICT
        self.character_dict = CHARACTER_DICT
        self.spell_dict = SPELL_DICT

        # Graphics
        self.background_color = self.game_dict["background_color"]
        self.background_image = load_image(self.graphics_folder, self.game_dict["background_image"])

        # Font
        self.ui_font = pygame.font.Font(self.game_dict["ui_font"], self.game_dict["ui_size"])
        self.status_font = pygame.font.Font(self.game_dict["status_font"], self.game_dict["status_size"])

        # Pause Screen
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

        # Image Effects
        self.effect_images = {}

        # Sound Effects
        self.sounds_effects = {}

        # Sound Voices
        self.sounds_voice = {}

        # Music
        self.music = None

        # Miscellaneous
        self.debug_color = self.game_dict["color"]["debug"]

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.characters = pygame.sprite.Group()
        self.spells = pygame.sprite.Group()
        self.impact = pygame.sprite.Group()

        self.player = Player(self, self.character_dict, "player", self.characters)
        self.enemy = Enemy(self, self.character_dict, "enemy", self.characters)

        self.paused = False
        self.debug_mode = True

    def run(self):
        self.playing = True
        if self.music is not None:
            pygame.mixer.music.load(path.join(music_folder, self.music))
            pygame.mixer.music.play(-1)
        while self.playing:
            self.dt = self.gameDisplay.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit_game(self):
        pygame.quit()
        quit()

    def events(self):
        self.event = pygame.event.get()
        for event in self.event:
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_h:
                    self.debug_mode = not self.debug_mode

                if event.key == pygame.K_LEFT:
                    self.player.buffer_move(dx=-1)
                if event.key == pygame.K_RIGHT:
                    self.player.buffer_move(dx=+1)
                if event.key == pygame.K_UP:
                    self.player.buffer_move(dy=-1)
                if event.key == pygame.K_DOWN:
                    self.player.buffer_move(dy=+1)

                if event.key == pygame.K_j:
                    self.enemy.move(dx=-1)
                if event.key == pygame.K_l:
                    self.enemy.move(dx=+1)
                if event.key == pygame.K_i:
                    self.enemy.move(dy=-1)
                if event.key == pygame.K_k:
                    self.enemy.move(dy=+1)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        draw_interface(self)
        draw_debug(self)
        draw_sprite(self)
        draw_status(self)

        # Pause
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")


        self.gameDisplay.update(self.event)

g = Game()
while True:
    g.run()
