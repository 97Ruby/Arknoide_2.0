""" Tela exibida quando o jogador perde as 3 vidas, vi essa tela tantas vezes que repensei o motivo da escolha desse tema de jogo. """

import pygame
from states.base_state import BaseState
from button import Button
from utils import draw_text
from config import COLOR_BG, COLOR_RED_TITLE, COLOR_WHITE
import sound_manager


class GameOverState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.score = 0
        self.level_number = 1
        self.retry_button = None
        self.menu_button = None
        self._layout_buttons()

    def _layout_buttons(self):
        w, h = self.app.screen.get_size()
        btn_width, btn_height = 220, 50
        cy = int(h * 0.62)
        self.retry_button = Button((w // 2 - btn_width - 10, cy, btn_width, btn_height), "REINICIAR", font_size=20)
        self.menu_button = Button((w // 2 + 10, cy, btn_width, btn_height), "MENU", font_size=20)

    def on_enter(self, score=0, level_number=1):
        self.score = score
        self.level_number = level_number
        self._layout_buttons()

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.retry_button.is_clicked(event):
            sound_manager.play_sfx("button_click")
            self.app.start_level(self.level_number)  # reinicia a mesma fase que o jogador perdeu, achei melhor que reeiniciar do zero
        elif self.menu_button.is_clicked(event):
            sound_manager.play_sfx("button_click")
            self.app.change_state("menu")

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.retry_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)

    def draw(self, surface):
        w, h = surface.get_size()
        surface.fill(COLOR_BG)
        self.app.starfield.draw(surface, (150, 60, 60))

        draw_text(surface, "GAME OVER", 56, COLOR_RED_TITLE, center=(w // 2, int(h * 0.32)))
        draw_text(surface, f"Pontuação final: {self.score:06d}", 24, COLOR_WHITE,
                  center=(w // 2, int(h * 0.46)))

        self.retry_button.draw(surface)
        self.menu_button.draw(surface)
