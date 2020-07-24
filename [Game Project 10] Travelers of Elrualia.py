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
        pygame.mixer.music.set_volume(default_volume/100)
        self.gameDisplay = ScaledGame(project_title, screen_size, FPS)
        self.dt = self.gameDisplay.clock.tick(FPS) / 1000
        self.load_data()
        self.new()
        self.update_stage()

    def update_sprite(self, sprite, move=False, keys=False):
        if move:
            sprite.update_move()
        if keys:
            sprite.get_keys()
        update_time_dependent(sprite)
        update_center(sprite)
        update_bobbing(sprite)

    def align_rect(self, surface, x, y, align):
        rect = surface.get_rect()
        if align == "nw":
            rect.topleft = (x, y)
        if align == "ne":
            rect.topright = (x, y)
        if align == "sw":
            rect.bottomleft = (x, y)
        if align == "se":
            rect.bottomright = (x, y)
        if align == "n":
            rect.midtop = (x, y)
        if align == "s":
            rect.midbottom = (x, y)
        if align == "e":
            rect.midright = (x, y)
        if align == "w":
            rect.midleft = (x, y)
        if align == "center":
            rect.center = (x, y)
        return rect

    def draw_text(self, text, font, color, pos, align="nw"):
        if not isinstance(text, str):
            text = str(text)
        text_surface = font.render(text, True, color)
        text_rect = self.align_rect(text_surface, int(pos[0]), int(pos[1]), align)
        if self.debug_mode:
            pygame.draw.rect(self.gameDisplay, CYAN, text_rect, 1)
        self.gameDisplay.blit(text_surface, text_rect)

    def draw_image(self, image, x, y, align="nw"):
        image_rect = self.align_rect(image, x, y, align)
        self.gameDisplay.blit(image, image_rect)

    def draw_shape(self, dict, object, text=None, dx=0, dy=0, dw=0, dh=0):
        # Settings ------------------- #
        object_dict = dict[object]
        settings_dict = dict[object_dict["type"]]
        rect = object_dict["rect"]
        shape = settings_dict["shape"]
        align = settings_dict["align"]
        color = settings_dict["color"]
        border_color = settings_dict["border_color"]
        border_size = settings_dict["border_size"]
        font = settings_dict["font"]
        font_color = settings_dict["font_color"]

        # Surface -------------------- #
        rect = [int(rect[0]+dx), int(rect[1]+dy), int(rect[2]+dw), int(rect[3]+dh)]
        surface = pygame.Surface((rect[2], rect[3]))
        surface_rect = self.align_rect(surface, rect[0], rect[1], align)
        if border_color is not None:
            surface.fill(border_color)
        shape(surface, color, (border_size, border_size, rect[2] - border_size*2, rect[3] - border_size*2))

        # Draw ----------------------- #
        self.gameDisplay.blit(surface, surface_rect)
        if text is not None and font is not None:
            self.draw_text(text, font, font_color, (rect[0], rect[1]), align)

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
        self.font_liberation = pygame.font.Font(path.join(self.font_folder, "LiberationSerif-Regular.ttf"), 40)
        self.ui_font = pygame.font.Font(self.game_dict["ui_font"], self.game_dict["ui_size"])
        self.status_font = pygame.font.Font(self.game_dict["status_font"], self.game_dict["status_size"])

        # Color
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
            "character_customization": {
                "game_status": "character_customization",
                "background": "background_chracter_customization.png",
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
            "type_1": {
                "center": True,
                "font": self.font_liberation, "font_color": WHITE,
                "inactive_color": LIGHTSKYBLUE, "active_color": DARKSKYBLUE, "border_color": BLACK, "border_size": 5,
                "sound_active": None, "sound_action": None},

            # Main Menu -------------- #
            "main_menu_new_game": {
                "rect": [640, 300, 280, 50], "type": "type_1", "text": "New Game"},
            "main_menu_load_game": {
                "rect": [640, 375, 280, 50], "type": "type_1", "text": "Load Game"},
            "main_menu_options": {
                "rect": [640, 450, 280, 50], "type": "type_1", "text": "Options"},
            "main_menu_exit": {
                "rect": [640, 525, 280, 50], "type": "type_1", "text": "Exit"},

            # Options ---------------- #
            "options_volume_down": {
                "rect": [487, 255, 75, 50], "type": "type_1", "text": "-5"},
            "options_volume_up": {
                "rect": [692, 255, 75, 50], "type": "type_1", "text": "+5"},
            "options_fullscreen": {
                "rect": [590, 325, 280, 50], "type": "type_1", "text": "Off/On"},
            "options_reset": {
                "rect": [180, 660, 280, 50], "type": "type_1", "text": "Reset to Default"},
            "options_confirm": {
                "rect": [590, 660, 280, 50], "type": "type_1", "text": "Confirm"},

            # Character Customization ---------- #
            "character_difficulty_left": {
                "rect": [82, 655, 75, 50], "type": "type_1", "text": "◄"},
            "character_difficulty_right": {
                "rect": [427, 655, 75, 50], "type": "type_1", "text": "►"},
            "character_health_down": {
                "rect": [992, 385, 75, 50], "type": "type_1", "text": "-5"},
            "character_health_up": {
                "rect": [1197, 385, 75, 50], "type": "type_1", "text": "+5"},
            "character_mana_down": {
                "rect": [992, 450, 75, 50], "type": "type_1", "text": "-1"},
            "character_mana_up": {
                "rect": [1197, 450, 75, 50], "type": "type_1", "text": "+1"},
            "character_energy_down": {
                "rect": [992, 515, 75, 50], "type": "type_1", "text": "-50"},
            "character_energy_up": {
                "rect": [1197, 515, 75, 50], "type": "type_1", "text": "+50"},
            "character_reset": {
                "rect": [685, 660, 280, 50], "type": "type_1", "text": "Reset to Default"},
            "character_confirm": {
                "rect": [1095, 660, 280, 50], "type": "type_1", "text": "Confirm"},
        }

        self.shape_dict = {
            "type_1": {
                "shape": pygame.draw.rect, "align": "center",
                "color": LIGHTSKYBLUE, "border_color": BLACK, "border_size": 5,
                "font": self.font_liberation, "font_color": WHITE},
            "type_2": {
                "shape": pygame.draw.rect, "align": "center",
                "color": SKYBLUE, "border_color": BLACK, "border_size": 5,
                "font": None, "font_color": None},
            "type_3": {
                "shape": pygame.draw.rect, "align": "center",
                "color": SKYBLUE, "border_color": None, "border_size": 0,
                "font": None, "font_color": None},
            "type_4": {
                "shape": pygame.draw.rect, "align": "nw",
                "color": LIGHTGREY, "border_color": None, "border_size": 0,
                "font": self.ui_font, "font_color": self.ui_color},

            # Options -------------------------- #
            "options_volume_1": {
                "rect": [180, 255, 280, 50], "type": "type_1"},
            "options_volume_2": {
                "rect": [590, 255, 130, 50], "type": "type_1"},
            "options_fullscreen": {
                "rect": [180, 325, 280, 50], "type": "type_1"},

            # Character Customization ---------- #
            "character_interface_1": {
                "rect": [255, 455, 480, 500], "type": "type_2"},
            "character_interface_2": {
                "rect": [890, 455, 750, 500], "type": "type_2"},
            "character_player": {
                "rect": [255, 255, 280, 50], "type": "type_1"},
            "character_difficulty": {
                "rect": [255, 655, 280, 50], "type": "type_1"},
            "character_level_1": {
                "rect": [685, 255, 280, 50], "type": "type_1"},
            "character_level_2": {
                "rect": [1095, 255, 280, 50], "type": "type_1"},
            "character_experience_1": {
                "rect": [685, 320, 280, 50], "type": "type_1"},
            "character_experience_2": {
                "rect": [1095, 320, 280, 50], "type": "type_1"},
            "character_health_1": {
                "rect": [685, 385, 280, 50], "type": "type_1"},
            "character_health_2": {
                "rect": [1095, 385, 280, 50], "type": "type_1"},
            "character_mana_1": {
                "rect": [685, 450, 280, 50], "type": "type_1"},
            "character_mana_2": {
                "rect": [1095, 450, 280, 50], "type": "type_1"},
            "character_energy_1": {
                "rect": [685, 515, 280, 50], "type": "type_1"},
            "character_energy_2": {
                "rect": [1095, 515, 280, 50], "type": "type_1"},
            "character_status_points_1": {
                "rect": [685, 580, 280, 50], "type": "type_1"},
            "character_status_points_2": {
                "rect": [1095, 580, 280, 50], "type": "type_1"},

            # Battle ----------------- #
            "battle_cursor": {
                "rect": [220, 360, 104, 54], "type": "type_3"},
            "battle_spell": {
                "rect": [50, 670, 40, 0], "type": "type_4"},
            "battle_mana": {
                "rect": [270, 630, 0, 40], "type": "type_4"},
            "battle_energy": {
                "rect": [420, 630, 0, 40], "type": "type_4"},
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
        if self.interface_image is not None and self.game_status == "battle":
            self.gameDisplay.blit(self.interface_image, (0, 0))


        # Interface ------------------ #
        if self.game_status == "options_menu":
            # Volume --------------------------- #
            self.draw_shape(self.shape_dict, "options_volume_1", "Volume")
            self.draw_shape(self.shape_dict, "options_volume_2", str(self.volume) + str("%"))
            self.draw_shape(self.shape_dict, "options_fullscreen", "Fullscreen")

        elif self.game_status == "character_customization":
            self.draw_shape(self.shape_dict, "character_interface_1")
            self.draw_shape(self.shape_dict, "character_interface_2")
            self.draw_shape(self.shape_dict, "character_player", "Player")
            self.draw_shape(self.shape_dict, "character_difficulty", "Difficulty")
            self.draw_shape(self.shape_dict, "character_level_1", "Level")
            self.draw_shape(self.shape_dict, "character_level_2", "Level")
            self.draw_shape(self.shape_dict, "character_experience_1", "Experience")
            self.draw_shape(self.shape_dict, "character_experience_2", "Experience")
            self.draw_shape(self.shape_dict, "character_health_1", "Heatlh")
            self.draw_shape(self.shape_dict, "character_health_2", "Heatlh")
            self.draw_shape(self.shape_dict, "character_mana_1", "Mana")
            self.draw_shape(self.shape_dict, "character_mana_2", "Mana")
            self.draw_shape(self.shape_dict, "character_energy_1", "Energy")
            self.draw_shape(self.shape_dict, "character_energy_2", "Energy")
            self.draw_shape(self.shape_dict, "character_status_points_1", "Status Points")
            self.draw_shape(self.shape_dict, "character_status_points_2", "Status Points")

        elif self.game_status == "battle":
            for sprite in self.characters:
                pygame.draw.rect(self.gameDisplay, sprite.debug_color, (int(sprite.debug_pos[0] + sprite.grid_pos[0] * sprite.grid_dt[0]), int(sprite.debug_pos[1] + sprite.grid_pos[1] * sprite.grid_dt[1]), sprite.debug_dt[0], sprite.debug_dt[1]))
            self.draw_shape(self.shape_dict, "battle_cursor", dx=(4+self.player.grid_pos[0]) * self.player.grid_dt[0], dy=self.player.grid_pos[1] * self.player.grid_dt[1])

            # Player --------------------------- #
            for index, cooldown in enumerate(self.player.cooldown):
                d_pos = 40*self.player.cooldown[cooldown]/self.player.spell_cooldown[cooldown]
                self.draw_shape(self.shape_dict, "battle_spell", dx=50*index, dy=-d_pos, dh=d_pos)
                self.draw_text(cooldown, self.ui_font, BLUE, (70+50*index, 650), "center")

            self.draw_shape(self.shape_dict, "battle_mana", dw=int(100 * self.player.mana / self.player.max_mana))
            self.draw_text(int(self.player.mana), self.ui_font, self.ui_color, self.player.mana_pos, "center")
            self.draw_text("Mana", self.ui_font, self.ui_color, (280, 635), "nw")

            self.draw_shape(self.shape_dict, "battle_energy", dw=int(100 * self.player.energy / self.player.max_energy))
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
                    Button(self, self.button_dict, "main_menu_new_game", self.buttons, action=self.update_stage, variable="character_customization")
                    Button(self, self.button_dict, "main_menu_load_game", self.buttons)
                    Button(self, self.button_dict, "main_menu_options", self.buttons, action=self.update_stage, variable="options_menu")
                    Button(self, self.button_dict, "main_menu_exit", self.buttons, action=self.quit_game)
                elif self.game_status == "options_menu":
                    Button(self, self.button_dict, "options_volume_down", self.buttons, action=self.update_volume, variable=-5)
                    Button(self, self.button_dict, "options_volume_up", self.buttons, action=self.update_volume, variable=+5)
                    Button(self, self.button_dict, "options_fullscreen", self.buttons)
                    Button(self, self.button_dict, "options_reset", self.buttons)
                    Button(self, self.button_dict, "options_confirm", self.buttons, action=self.update_stage, variable=self.previous_status)
                elif self.game_status == "character_customization":
                    Button(self, self.button_dict, "character_difficulty_left", self.buttons, action=self.update_volume, variable=-1)
                    Button(self, self.button_dict, "character_difficulty_right", self.buttons, action=self.update_volume, variable=+1)
                    Button(self, self.button_dict, "character_health_down", self.buttons, action=self.update_volume, variable=-5)
                    Button(self, self.button_dict, "character_health_up", self.buttons, action=self.update_volume, variable=+5)
                    Button(self, self.button_dict, "character_mana_down", self.buttons, action=self.update_volume, variable=-1)
                    Button(self, self.button_dict, "character_mana_up", self.buttons, action=self.update_volume, variable=+1)
                    Button(self, self.button_dict, "character_energy_down", self.buttons, action=self.update_volume, variable=-50)
                    Button(self, self.button_dict, "character_energy_up", self.buttons, action=self.update_volume, variable=+50)
                    Button(self, self.button_dict, "character_reset", self.buttons)
                    Button(self, self.button_dict, "character_confirm", self.buttons, action=self.update_stage, variable="battle_1")
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
