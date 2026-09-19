""" Tela exibida quando o jogador destrói todos os blocos de uma fase.
Oferece avançar para a próxima fase (se houver) ou voltar ao menu. Fora a musiquinha de vitória que toca. """

import pygame
from states.base_state import BaseState
from button import Button
from utils import draw_text
from config import COLOR_BG, COLOR_YELLOW, COLOR_WHITE
from levels import TOTAL_LEVELS
import sound_manager


class VictoryState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.score = 0
        self.level_number = 1
        self.next_button = None
        self.menu_button = None
        self._layout_buttons()

    def _layout_buttons(self):
        w, h = self.app.screen.get_size()
        btn_width, btn_height = 220, 50
        cy = int(h * 0.62)
        has_next = self.level_number < TOTAL_LEVELS
        next_label = "PRÓXIMA FASE" if has_next else "MENU"
        self.next_button = Button((w // 2 - btn_width - 10, cy, btn_width, btn_height), next_label, font_size=20)
        self.menu_button = Button((w // 2 + 10, cy, btn_width, btn_height), "MENU", font_size=20)

    def on_enter(self, score=0, level_number=1):
        self.score = score
        self.level_number = level_number
        self._layout_buttons()

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.next_button.is_clicked(event):
            sound_manager.play_sfx("button_click")
            if self.level_number < TOTAL_LEVELS:
                self.app.start_level(self.level_number + 1)
            else:
                self.app.change_state("menu")
        elif self.menu_button.is_clicked(event):
            sound_manager.play_sfx("button_click")
            self.app.change_state("menu")

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.next_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)

    def draw(self, surface):
        w, h = surface.get_size()
        surface.fill(COLOR_BG)
        self.app.starfield.draw(surface, (255, 230, 150))

        draw_text(surface, "FASE CONCLUÍDA!", 48, COLOR_YELLOW, center=(w // 2, int(h * 0.32)))
        draw_text(surface, f"Pontuação: {self.score:06d}", 24, COLOR_WHITE,
                  center=(w // 2, int(h * 0.46)))

        self.next_button.draw(surface)
        if self.level_number < TOTAL_LEVELS:
            self.menu_button.draw(surface)
