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

    def update_sprite(self, sprite):
        sprite.rect.x, sprite.rect.y = int(sprite.pos[0]), int(sprite.pos[1])
        if sprite.tile:
            update_time_dependent(sprite)
        if sprite.bobbing:
            update_bobbing(sprite)

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.graphics_folder = path.join(self.data_folder, "graphics")
        self.sfx_folder = path.join(self.data_folder, "sfx")
        self.voice_folder = path.join(self.data_folder, "voice")
        self.music_folder = path.join(self.data_folder, "music")
        self.map_folder = path.join(self.data_folder, "map")

        # Font
        self.font = None

        # Pause Screen
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

        # Graphics
        self.background_battle_img = load_image(self.graphics_folder, BACKGROUND_BATTLE_IMG)

        # Item Images
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = load_image(self.graphics_folder, ITEM_IMAGES[item])

        # Spell Images
        self.spell_images = {}
        for item in SPELL_DICT:
            self.spell_images[item] = load_image(self.graphics_folder, SPELL_DICT[item]["image"])

        # Passive Images
        self.passive_images = {}
        for item in PASSIVE_DICT:
            self.passive_images[item] = load_image(self.graphics_folder, PASSIVE_DICT[item]["image"])

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
        self.items = pygame.sprite.Group()

        self.player = Player(self, CHARACTER_DICT, GAME_DICT, "player")
        self.enemy = Enemy(self, ENEMY_DICT, UI_DICT, "Skeleton")

    def run(self):
        self.playing = True
        if self.music is not None:
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
                    self.player.move(dx=-1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(dx=+1)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(dy=-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(dy=+1)

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
        # Background
        self.gameDisplay.fill(BACKGROUND_COLOR)
        self.gameDisplay.blit(self.background_battle_img, (0, 0))

        # Interface
        for sprite in self.characters:
            sprite.draw_ui()

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
    g.run()
