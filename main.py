""" Ponto de entrada do jogo. A classe App inicializa a janela, o mixer de som e o dicionário de estados (telas), e roda o loop principal repassando eventos/update/draw para o estado ativo no momento. """

import ctypes
import os
import sys

import pygame

import config
import sound_manager
from utils import Starfield
from states.menu_state import MenuState
from states.phase_select_state import PhaseSelectState
from states.settings_state import SettingsState
from states.game_state import GameState
from states.game_over_state import GameOverState
from states.victory_state import VictoryState

# Faz o SDL sempre abrir a janela centralizada no monitor, tanto rodando via script quanto empacotado em .exe
os.environ["SDL_VIDEO_CENTERED"] = "1"

if sys.platform == "win32":
    try:
        # Sem isso, o Windows aplica escalonamento de DPI virtual na
        # janela do jogo em telas de alta densidade, deixando o layout
        # borrado/desalinhado
        ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
        pass


class App:
    def __init__(self):
        pygame.init()
        sound_manager.init()

        self.settings = config.load_save_data()
        self.max_unlocked_level = self.settings["max_unlocked_level"]
        self.stars = self.settings["stars"]

        resolution = tuple(self.settings["resolution"])
        fullscreen = bool(self.settings.get("fullscreen", False))
        pygame.display.set_caption(config.GAME_TITLE)
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode(resolution, flags)
        self.starfield = Starfield(*resolution)
        self.clock = pygame.time.Clock()

        self.states = {
            "menu": MenuState(self),
            "phase_select": PhaseSelectState(self),
            "settings": SettingsState(self),
            "game": GameState(self),
            "game_over": GameOverState(self),
            "victory": VictoryState(self),
        }
        self.state_name = "menu"
        self.states[self.state_name].on_enter()

    def change_state(self, name, **kwargs):
        self.state_name = name
        self.states[name].on_enter(**kwargs)

    def start_level(self, level_number):
        self.change_state("game")
        self.states["game"].start_level(level_number)

    def unlock_next_level(self, level_number):
# Marca a fase concluída com estrela e destrava a próxima.
        self.stars[str(level_number)] = True
        if level_number + 1 > self.max_unlocked_level:
            self.max_unlocked_level = level_number + 1
        self._persist_settings()

    def apply_resolution(self, resolution):
        self.apply_display_settings(resolution=resolution)

    def apply_display_settings(self, resolution=None, fullscreen=None):
        if resolution is None:
            resolution = tuple(self.settings["resolution"])
        if fullscreen is None:
            fullscreen = bool(self.settings.get("fullscreen", False))

        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode(resolution, flags)
        self.starfield = Starfield(*resolution)
        self.settings["resolution"] = list(resolution)
        self.settings["fullscreen"] = bool(fullscreen)
        self._persist_settings()

    def _persist_settings(self):
        self.settings["max_unlocked_level"] = self.max_unlocked_level
        self.settings["stars"] = self.stars
        config.save_save_data(self.settings)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(config.FPS) / 1000.0
            current_state = self.states[self.state_name]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    current_state.handle_event(event)

            current_state.update(dt)
            current_state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    App().run()
