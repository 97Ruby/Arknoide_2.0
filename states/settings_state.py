""" Permite ao usuário escolher a resolução da janela entre os presets
definidos em config.RESOLUTION_PRESETS, resolução pode ser
ajustáda pelo usuário sem expor uma caixa de texto livre (entre ospresets já definidos). """

import pygame
from states.base_state import BaseState
from button import Button
from utils import draw_text
from config import COLOR_BG, COLOR_NEON_BLUE, RESOLUTION_PRESETS
import sound_manager


class SettingsState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.resolution_buttons = []
        self.back_button = None
        self._layout_buttons()

    def _layout_buttons(self):
        w, h = self.app.screen.get_size()
        btn_width = 240
        btn_height = 50
        gap = 20
        start_y = int(h * 0.35)

        self.resolution_buttons = []
        for i, (rw, rh) in enumerate(RESOLUTION_PRESETS):
            rect = (w // 2 - btn_width // 2, start_y + i * (btn_height + gap), btn_width, btn_height)
            label = f"{rw} x {rh}"
            self.resolution_buttons.append(((rw, rh), Button(rect, label, font_size=20)))

        self.back_button = Button((24, h - 60, 120, 40), "VOLTAR", font_size=18)

    def on_enter(self):
        self._layout_buttons()

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.back_button.is_clicked(event):
            sound_manager.play_sfx("button_click")
            self.app.change_state("menu")
            return
        for resolution, btn in self.resolution_buttons:
            if btn.is_clicked(event):
                sound_manager.play_sfx("button_click")
                self.app.apply_resolution(resolution)
                self._layout_buttons()
                return

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        for _, btn in self.resolution_buttons:
            btn.update(mouse_pos)

    def draw(self, surface):
        w, h = surface.get_size()
        surface.fill(COLOR_BG)
        self.app.starfield.draw(surface, (200, 210, 255))
        draw_text(surface, "CONFIGURAÇÕES", 32, COLOR_NEON_BLUE, center=(w // 2, int(h * 0.16)))
        draw_text(surface, "Resolução da janela:", 18, (200, 205, 230), center=(w // 2, int(h * 0.27)))

        current = tuple(self.app.settings["resolution"])
        for resolution, btn in self.resolution_buttons:
            btn.draw(surface)
            if resolution == current:
                draw_text(surface, "(atual)", 14, (120, 255, 150),
                          center=(btn.rect.centerx, btn.rect.bottom + 14))

        self.back_button.draw(surface)
