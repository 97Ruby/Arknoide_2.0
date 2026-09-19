""" Grid de seleção de fase (1 a 16). Fases além da
max_unlocked_level aparecem desabilitadas (cinza), o jogador precisa concluir uma fase para destravar a próxima. Fases já concluídas mostram uma estrela. """

import pygame
from states.base_state import BaseState
from button import Button
from utils import draw_text
from config import COLOR_BG, COLOR_NEON_BLUE, COLOR_YELLOW
from levels import TOTAL_LEVELS
import sound_manager


class PhaseSelectState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.level_buttons = []
        self.back_button = None
        self._layout_buttons()

    def _layout_buttons(self):
        w, h = self.app.screen.get_size()
        cols = 4
        rows = (TOTAL_LEVELS + cols - 1) // cols
        gap = 16
        start_y = int(h * 0.30)

        # Reserva espaço para o botão VOLTAR no rodapé e limita a grade a essa
        # altura disponível, evitando que ela invada o botão em resoluções
        # menores.
        back_button_area = 80
        available_height = h - start_y - back_button_area
        max_by_height = (available_height - (rows - 1) * gap) // rows
        btn_size = max(36, min(int(w * 0.14), 90, int(max_by_height)))
        grid_width = cols * btn_size + (cols - 1) * gap
        grid_height = rows * btn_size + (rows - 1) * gap
        start_x = w // 2 - grid_width // 2

        self.level_buttons = []
        for i in range(TOTAL_LEVELS):
            level_number = i + 1
            col = i % cols
            row = i // cols
            x = start_x + col * (btn_size + gap)
            y = start_y + row * (btn_size + gap)
            enabled = level_number <= self.app.max_unlocked_level
            btn = Button((x, y, btn_size, btn_size), str(level_number), font_size=22, enabled=enabled)
            self.level_buttons.append((level_number, btn))

        self.back_button = Button((24, h - 60, 120, 40), "VOLTAR", font_size=18)

        self._grid_bottom = start_y + grid_height

    def on_enter(self):
        self._layout_buttons()

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.back_button.is_clicked(event):
            sound_manager.play_sfx("button_click")
            self.app.change_state("menu")
            return
        for level_number, btn in self.level_buttons:
            if btn.is_clicked(event):
                sound_manager.play_sfx("button_click")
                self.app.start_level(level_number)
                return

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        for _, btn in self.level_buttons:
            btn.update(mouse_pos)

    def draw(self, surface):
        w, h = surface.get_size()
        surface.fill(COLOR_BG)
        self.app.starfield.draw(surface, (200, 210, 255))
        draw_text(surface, "SELEÇÃO DE FASE", 32, COLOR_NEON_BLUE, center=(w // 2, int(h * 0.14)))

        for level_number, btn in self.level_buttons:
            btn.draw(surface)
            if str(level_number) in self.app.stars:
                draw_text(surface, "*", 20, COLOR_YELLOW,
                          center=(btn.rect.centerx, btn.rect.bottom + 10))

        self.back_button.draw(surface)
