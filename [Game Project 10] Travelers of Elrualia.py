import pygame
import os
from pygame.locals import *
from os import path

from Settings import *
from ScaledGame import *
from Camera import *
from Map import *
from Function import *
from Class import *

vec = pygame.math.Vector2

# Characters Settings
PLAYER_IMG = "character_pipoya_male_01_2.png"


"""
    Game
"""
class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        pygame.key.set_repeat(300, 75)
        self.gameDisplay = ScaledGame(project_title, screen_size, FPS)
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000
        self.load_data()
        self.new()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pygame.font.Font(font_name, size)
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
        self.gameDisplay.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        data_folder = path.join(game_folder, "data")
        graphics_folder = path.join(data_folder, "graphics")
        sfx_folder = path.join(data_folder, "sfx")
        voice_folder = path.join(data_folder, "voice")
        music_folder = path.join(data_folder, "music")
        map_folder = path.join(data_folder, "map")

        # Font
        self.font = None

        # Pause Screen
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

        # Map

        # Characters
        self.player_img = load_tile_table(path.join(graphics_folder, PLAYER_IMG), 32, 32)

        # Image Items
        self.item_images = {}

        # Image Effects
        self.effect_images = {}

        # Sound Effects
        self.sounds_effects = {}

        # Sound Voices
        self.sounds_voice = {}

        # Music
        self.music = None

    def new(self):
        self.paused = False
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.characters = pygame.sprite.Group()

        self.player = Player(self, WIDTH/2, HEIGHT/2, self.player_img, "Player")
        self.cursor = Cursor(self, WIDTH/2, HEIGHT/2-8)

    def run(self):
        self.playing = True
        if self.music != None:
            pygame.mixer.music.load(path.join(music_folder, self.music))
            pygame.mixer.music.play(-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
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

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.cursor.move(dx=-1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.cursor.move(dx=+1)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.cursor.move(dy=-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.cursor.move(dy=+1)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.gameDisplay.fill(LIGHTGREY)

        # Sprite
        for sprite in self.all_sprites:
            self.gameDisplay.blit(sprite.image, sprite)

        # Pause
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        self.gameDisplay.update(self.event)

g = Game()
while True:
    g.new()
    g.run()
