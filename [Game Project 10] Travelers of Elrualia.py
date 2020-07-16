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
        pygame.mixer.music.set_volume(0.075)
        self.update_stage()

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
        self.button_dict = BUTTON_DICT
        self.character_dict = CHARACTER_DICT
        self.spell_dict = SPELL_DICT
        self.stage_dict = STAGE_DICT

        # Graphics
        self.background_image = None
        self.background_color = self.game_dict["background_color"]
        self.interface_image = load_image(self.graphics_folder, self.game_dict["interface_image"])

        # Font
        self.font = pygame.font.Font(None, 100)
        self.main_menu_font = pygame.font.Font(self.game_dict["main_menu_font"], self.game_dict["main_menu_size"])
        self.button_font = pygame.font.Font(self.game_dict["button_font"], self.game_dict["button_size"])
        self.ui_font = pygame.font.Font(self.game_dict["ui_font"], self.game_dict["ui_size"])
        self.status_font = pygame.font.Font(self.game_dict["status_font"], self.game_dict["status_size"])

        # Color
        self.main_menu_color = self.game_dict["main_menu_color"]
        self.button_color = self.game_dict["button_color"]
        self.ui_color = self.game_dict["ui_color"]

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
        self.project_title = project_title
        self.debug_color = self.game_dict["color"]["debug"]

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.characters = pygame.sprite.Group()
        self.spells = pygame.sprite.Group()
        self.impact = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.paused = False

        # Debug ---------------------- #
        self.debug_mode = True
        self.debug_stage = []
        self.debug_stage_index = 0
        for stage in self.stage_dict:
            self.debug_stage.append(stage)

    # Game Loop ---------------------- #
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.gameDisplay.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        self.quit_game()

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
                if event.key == pygame.K_j:
                    self.debug_stage_index = (self.debug_stage_index + 1) % len(self.debug_stage)
                    self.update_stage(self.debug_stage[self.debug_stage_index])

                if self.game_status == "battle":
                    if event.key == pygame.K_LEFT:
                        self.player.buffer_move(dx=-1)
                    if event.key == pygame.K_RIGHT:
                        self.player.buffer_move(dx=+1)
                    if event.key == pygame.K_UP:
                        self.player.buffer_move(dy=-1)
                    if event.key == pygame.K_DOWN:
                        self.player.buffer_move(dy=+1)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        # Background ----------------- #
        self.gameDisplay.fill(self.background_color)
        self.gameDisplay.blit(self.background_image, (0, 0))

        # Main Menu ------------------ #
        if self.game_status == "main_menu":
            self.draw_text(self.project_title, self.main_menu_font, self.main_menu_color, (WIDTH/2, HEIGHT/5), "center", self.debug_mode)

            # Sprite
            for sprite in self.all_sprites:
                self.gameDisplay.blit(sprite.image, sprite)

            for button in self.buttons:
                button.draw_text()

        # Battle --------------------- #
        if self.game_status == "battle":
            # Interface
            self.gameDisplay.blit(self.interface_image, (0, 0))
            for sprite in self.characters:
                pygame.draw.rect(self.gameDisplay, sprite.debug_color, (int(sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0]), int(sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1]), sprite.debug_dt[0], sprite.debug_dt[1]))
                sprite.draw_ui()
            pygame.draw.rect(self.gameDisplay, self.game_dict["color"]["cursor"], (int(self.player.debug_pos[0] + (self.player.grid_pos[0]+4) * self.player.grid_dt[0]), int(self.player.debug_pos[1] + self.player.grid_pos[1] * self.player.grid_dt[1]), self.player.debug_dt[0], self.player.debug_dt[1]))

            # Debug
            if self.debug_mode:
                for sprite in self.all_sprites:
                    pygame.draw.rect(self.gameDisplay, self.debug_color, sprite.rect, 1)
                for sprite in self.characters:
                    sprite.draw_debug()
                    pygame.draw.rect(self.gameDisplay, sprite.debug_color, (int(sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0]), int(sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1]), sprite.debug_dt[0], sprite.debug_dt[1]), 1)

            # Sprite
            for sprite in self.all_sprites:
                self.gameDisplay.blit(sprite.image, sprite)

            # Status
            for sprite in self.characters:
                sprite.draw_status()
                self.draw_text(sprite.health, self.status_font, sprite.status_color, sprite.pos + sprite.hp_offset, "center", self.debug_mode)

        # Pause ---------------------- #
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, RED, (WIDTH / 2, HEIGHT / 2), align="center")

        self.gameDisplay.update(self.event)

    # Gameplay ----------------------- #
    def update_stage(self, stage="main_menu"):
        self.stage = self.stage_dict[stage]
        self.game_status = self.stage["game_status"]
        self.update_background(self.stage["background"])
        self.update_music(self.stage["music"])

        if self.game_status == "main_menu":
            Button(self, self.button_dict, "start", self.buttons, "Start", self.button_font, self.button_color)
            Button(self, self.button_dict, "options", self.buttons, "Options", self.button_font, self.button_color, variable="options_menu", action=self.update_stage)
            Button(self, self.button_dict, "exit", self.buttons, "Exit", self.button_font, self.button_color, action=self.quit_game)
        elif self.game_status == "options_menu":
            pass
        elif self.game_status == "battle":
            self.player = Player(self, self.character_dict, "player", self.characters)
            self.enemy = Enemy(self, self.character_dict, "enemy", self.characters)

    def update_background(self, background):
        if background is not None:
            background = load_image(self.graphics_folder, background)
            if self.background_image != background:
                self.background_image = background

    def update_music(self, music):
        if music is not None:
            music = path.join(self.music_folder, music)
            if self.music != music:
                self.music = music
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)


g = Game()
while True:
    g.run()
