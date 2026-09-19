""" Botão retangular clicável usado em todas as telas de menu (Menu Principal,
Fases, Configurações, Game Over, Vitória). Isei para centralizar a lógica para evitar
recriar em cada um dos estados. """

import pygame
from utils import draw_text, draw_glow_rect
from config import COLOR_NEON_BLUE, COLOR_WHITE


class Button:
    def __init__(self, rect, label, font_size=24, enabled=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font_size = font_size
        self.enabled = enabled
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        """ É chamado chamado a partir de um evento MOUSEBUTTONDOWN (botão
        esquerdo). Retorna True só quando o botão está habilitado e o
        clique foi dentro do retângulo. """
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        if not self.enabled:
            fill = (25, 25, 40)
            border = (70, 70, 90)
            text_color = (110, 110, 130)
        elif self.hovered:
            fill = (20, 60, 90)
            border = COLOR_NEON_BLUE
            text_color = COLOR_WHITE
            draw_glow_rect(surface, self.rect, COLOR_NEON_BLUE, glow_layers=3)
        else:
            fill = (12, 30, 55)
            border = (0, 120, 160)
            text_color = COLOR_WHITE

        pygame.draw.rect(surface, fill, self.rect, border_radius=8)
        pygame.draw.rect(surface, border, self.rect, width=2, border_radius=8)
        draw_text(surface, self.label, self.font_size, text_color, center=self.rect.center)
