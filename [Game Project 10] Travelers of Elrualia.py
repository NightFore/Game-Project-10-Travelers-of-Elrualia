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
        pygame.mixer.music.set_volume(default_volume/100)
        self.update_stage()

    def update_sprite(self, sprite, move=False, keys=False):
        if move:
            sprite.update_move()
        if keys:
            sprite.get_keys()
        update_time_dependent(sprite)
        update_center(sprite)
        update_bobbing(sprite)

    def draw_text(self, text, font, color, pos, align="nw"):
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
        if self.debug_mode:
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
        self.font_folder = path.join(self.data_folder, "fonts")

        # Dict
        self.game_dict = GAME_DICT
        self.character_dict = CHARACTER_DICT
        self.spell_dict = SPELL_DICT

        # Graphics
        self.background_image = None
        self.background_color = self.game_dict["background_color"]
        self.interface_image = load_image(self.graphics_folder, self.game_dict["interface_image"])

        # Font
        self.font = pygame.font.Font(None, 100)
        self.main_menu_font = pygame.font.Font(self.game_dict["main_menu_font"], self.game_dict["main_menu_size"])
        self.ui_font = pygame.font.Font(self.game_dict["ui_font"], self.game_dict["ui_size"])
        self.status_font = pygame.font.Font(self.game_dict["status_font"], self.game_dict["status_size"])

        # Color
        self.main_menu_color = self.game_dict["main_menu_color"]
        self.button_color = self.game_dict["button_color"]
        self.ui_color = self.game_dict["ui_color"]
        self.status_color = self.game_dict["status_color"]

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
        self.default_volume = default_volume
        self.volume = self.default_volume
        self.game_status = None
        self.previous_status = None
        self.debug_color = self.game_dict["color"]["debug"]

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.characters = pygame.sprite.Group()
        self.spells = pygame.sprite.Group()
        self.impact = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.player = Player(self, self.character_dict, "player", self.characters)
        self.difficulty = "Normal"

        self.paused = False

        # Colors --------------------- #
        self.button_inactive = 140, 205, 245
        self.button_active = 15, 160, 240

        # Font ---------------------- #
        self.button_font = pygame.font.Font(path.join(self.font_folder, self.game_dict["button_font"]), self.game_dict["button_size"])

        # Dictionaries --------------- #
        self.stage_dict = {
            "main_menu": {
                "game_status": "main_menu",
                "background": "background_main_menu.png",
                "music": "PerituneMaterial_Whisper_loop.ogg"},
            "options_menu": {
                "game_status": "options_menu",
                "background": "background_options.png",
                "music": "PerituneMaterial_Whisper_loop.ogg"},
            "dialogue_1": {
                "game_status": "battle",
                "background": "craftpix_Battleground3_bright.png",
                "music": "PerituneMaterial_Prairie_loop.ogg",
                "enemy": ["enemy"]},
            "battle_1": {
                "game_status": "battle",
                "background": "craftpix_Battleground3_bright.png",
                "music": "PerituneMaterial_Prairie4_loop.ogg",
                "enemy": ["enemy", "enemy"]},
            "boss_1": {
                "game_status": "battle",
                "background": "craftpix_Battleground3_pale.png",
                "music": "PerituneMaterial_Rapid4_loop.ogg",
                "enemy": ["enemy", "enemy"]}
        }

        self.button_dict = {
            "new_game": {
                "pos": [640, 300], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "load_game": {
                "pos": [640, 375], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "options": {
                "pos": [640, 450], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "exit": {
                "pos": [640, 525], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "return": {
                "pos": [1190, 690], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "options_volume_down": {
                "pos": [487, 255], "width": 75, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "options_volume_up": {
                "pos": [692, 255], "width": 75, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "options_fullscreen": {
                "pos": [590, 325], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "options_reset": {
                "pos": [180, 660], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
            "options_confirm": {
                "pos": [590, 660], "width": 280, "height": 50, "border_size": 5, "border_color": BLACK, "center": True,
                "inactive": self.button_inactive, "active": self.button_active, "font": self.button_font, "color": self.button_color,
                "sound_active": None, "sound_action": None},
        }

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
        self.click = [False, False, False]
        for event in self.event:
            self.mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click[event.button] = True

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
        self.buttons.update()
        self.all_sprites.update()

    def draw(self):
        # Background ----------------- #
        self.gameDisplay.fill(self.background_color)
        if self.background_image is not None:
            self.gameDisplay.blit(self.background_image, (0, 0))

        # Interface ------------------ #
        if self.game_status == "options_menu":
            self.draw_text("Volume", self.button_font, self.button_color, (180, 255), "center")
            self.draw_text(str(self.volume) + str("%"), self.button_font, self.button_color, (590, 255), "center")
            self.draw_text("Fullscreen", self.button_font, self.button_color, (180, 325), "center")

        if self.game_status == "battle":
            self.gameDisplay.blit(self.interface_image, (0, 0))
            for sprite in self.characters:
                pygame.draw.rect(self.gameDisplay, sprite.debug_color, (int(sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0]), int(sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1]), sprite.debug_dt[0], sprite.debug_dt[1]))
            pygame.draw.rect(self.gameDisplay, self.game_dict["color"]["cursor"], (int(self.player.debug_pos[0] + (self.player.grid_pos[0]+4) * self.player.grid_dt[0]), int(self.player.debug_pos[1] + self.player.grid_pos[1] * self.player.grid_dt[1]), self.player.debug_dt[0], self.player.debug_dt[1]))

            # Player --------------------------- #
            index = 0
            for cooldown in self.player.cooldown:
                pygame.draw.rect(self.gameDisplay, LIGHTGREY, (50+50*index, 670, 40, int(-40 * self.player.cooldown[cooldown] / self.player.spell_cooldown[cooldown])))
                self.draw_text(cooldown, self.ui_font, BLUE, (70+50*index, 650), "center")
                index += 1

            pygame.draw.rect(self.gameDisplay, LIGHTGREY, (270, 630, int(100 * self.player.mana / self.player.max_mana), 40))
            self.draw_text(int(self.player.mana), self.ui_font, self.ui_color, self.player.mana_pos, "center")
            self.draw_text("Mana", self.ui_font, self.ui_color, (280, 635), "nw")

            pygame.draw.rect(self.gameDisplay, LIGHTGREY, (420, 630, int(100 * self.player.energy / self.player.max_energy), 40))
            self.draw_text(int(self.player.energy), self.ui_font, self.ui_color, self.player.energy_pos, "center")
            self.draw_text("Energy", self.ui_font, self.ui_color, (420, 635), "nw")

            # Debug
            if self.debug_mode:
                for sprite in self.all_sprites:
                    pygame.draw.rect(self.gameDisplay, self.debug_color, sprite.rect, 1)
                for sprite in self.characters:
                    pygame.draw.rect(self.gameDisplay, sprite.debug_color, (int(sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0]), int(sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1]), sprite.debug_dt[0], sprite.debug_dt[1]), 1)

                pygame.draw.rect(self.gameDisplay, CYAN, (50, 670, 40, -40), 1)
                pygame.draw.rect(self.gameDisplay, CYAN, (50, 670, 40, -40 * self.player.cooldown["Q"] / self.spell_dict["energy_ball"]["cooldown"]), 1)
                pygame.draw.rect(self.gameDisplay, CYAN, (100, 670, 40, -40), 1)
                pygame.draw.rect(self.gameDisplay, CYAN, (100, 670, 40, -40 * self.player.cooldown["W"] / self.spell_dict["thunder"]["cooldown"]), 1)
                pygame.draw.rect(self.gameDisplay, CYAN, (150, 670, 40, -40), 1)
                pygame.draw.rect(self.gameDisplay, CYAN, (150, 670, 40, -40 * self.player.cooldown["E"] / self.spell_dict["projectile"]["cooldown"]), 1)


        # Sprites -------------------- #
        for button in self.buttons:
            button.draw()
        for sprite in self.all_sprites:
            sprite.draw()

        # Pause ---------------------- #
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, RED, (WIDTH / 2, HEIGHT / 2), align="center")

        self.gameDisplay.update(self.event)

    # Gameplay ----------------------- #
    def update_stage(self, stage="main_menu"):
        self.stage = self.stage_dict[stage]
        self.update_status(self.stage["game_status"])
        self.update_background(self.stage["background"])
        self.update_music(self.stage["music"])

    def update_status(self, status):
        if status is not None:
            if self.game_status != status:
                self.previous_status = self.game_status
                self.game_status = status

                for button in self.buttons:
                    button.kill()

                if self.game_status == "main_menu":
                    Button(self, self.button_dict, "new_game", self.buttons, "New Game", action=self.update_stage, variable="battle_1")
                    Button(self, self.button_dict, "load_game", self.buttons, "Load Game")
                    Button(self, self.button_dict, "options", self.buttons, "Options", action=self.update_stage, variable="options_menu")
                    Button(self, self.button_dict, "exit", self.buttons, "Exit", action=self.quit_game)
                elif self.game_status == "options_menu":
                    Button(self, self.button_dict, "options_volume_down", self.buttons, "-5", action=self.update_volume, variable=-5)
                    Button(self, self.button_dict, "options_volume_up", self.buttons, "+5", action=self.update_volume, variable=+5)
                    Button(self, self.button_dict, "options_fullscreen", self.buttons, "Off/On")
                    Button(self, self.button_dict, "options_reset", self.buttons, "Reset to Default")
                    Button(self, self.button_dict, "options_confirm", self.buttons, "Confirm", action=self.update_stage, variable=self.previous_status)
                elif self.game_status == "character_customization":
                    pass
                elif self.game_status == "battle":
                    for enemy in self.characters:
                        if enemy.object != "player":
                            enemy.kill()
                    for enemy in self.stage["enemy"]:
                        self.enemy = Enemy(self, self.character_dict, enemy, self.characters)

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

    def update_volume(self, dv=0):
        if 0 <= self.volume + dv <= 100:
            self.volume = self.volume + dv
            pygame.mixer.music.set_volume(self.volume/100)



g = Game()
while True:
    g.run()
