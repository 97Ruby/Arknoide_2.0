""" Tela inicial: título do jogo + botões JOGAR / FASES / CONFIGURAÇÕES / SAIR. """

import sys
import pygame
from states.base_state import BaseState
from button import Button
from utils import draw_text
from config import COLOR_BG, COLOR_RED_TITLE, GAME_TITLE
import sound_manager


class MenuState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = {}
        self._layout_buttons()

    def _layout_buttons(self):
        w, h = self.app.screen.get_size()
        cx = w // 2
        btn_width = int(w * 0.32)
        btn_height = 46
        start_y = int(h * 0.56)
        gap = 16

        labels = ["JOGAR", "FASES", "CONFIGURAÇÕES", "SAIR"]
        self.buttons = {}
        for i, label in enumerate(labels):
            rect = (cx - btn_width // 2, start_y + i * (btn_height + gap), btn_width, btn_height)
            self.buttons[label] = Button(rect, label, font_size=22)

    def on_enter(self):
        # Recalcula posições dos botões (a resolução pode ter mudado na tela
        # de Configurações desde a última vez que este menu apareceu).
        self._layout_buttons()
        sound_manager.play_music("menu_music")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["JOGAR"].is_clicked(event):
                sound_manager.play_sfx("button_click")
                self.app.start_level(self.app.max_unlocked_level)
            elif self.buttons["FASES"].is_clicked(event):
                sound_manager.play_sfx("button_click")
                self.app.change_state("phase_select")
            elif self.buttons["CONFIGURAÇÕES"].is_clicked(event):
                sound_manager.play_sfx("button_click")
                self.app.change_state("settings")
            elif self.buttons["SAIR"].is_clicked(event):
                pygame.quit()
                sys.exit(0)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update(mouse_pos)

    def draw(self, surface):
        w, h = surface.get_size()
        surface.fill(COLOR_BG)
        self.app.starfield.draw(surface, (200, 210, 255))

        draw_text(surface, GAME_TITLE, min(64, w // 9), COLOR_RED_TITLE, center=(w // 2, int(h * 0.28)))
        draw_text(surface, "Arcade Retro - quebre todos os blocos!", 16, (180, 190, 220),
                  center=(w // 2, int(h * 0.28) + 46))

        for button in self.buttons.values():
            button.draw(surface)
