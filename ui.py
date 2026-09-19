""" Desenha a barra de HUD (pontuação, fase, vidas) e a moldura neon da área
jogável, replicando o topo da tela os coraçõeszinhos de vida  <3 <3 <3". """

import pygame
from config import COLOR_NEON_BLUE, COLOR_WHITE, COLOR_YELLOW
from utils import draw_text


def draw_hud(surface, score, level_number, lives, hud_rect):
    """Desenha a barra superior. Recebe hud_rect para já se adaptar caso a resolução da janela mude (a barra sempre ocupa a largura da tela)."""
    pygame.draw.rect(surface, (10, 12, 40), hud_rect)
    pygame.draw.line(surface, COLOR_NEON_BLUE, (0, hud_rect.bottom), (hud_rect.width, hud_rect.bottom), 2)

    score_text = f"SCORE {score:06d}"
    draw_text(surface, score_text, 22, COLOR_WHITE, topleft=(24, hud_rect.height // 2 - 14))

    phase_text = f"FASE {level_number}"
    draw_text(surface, phase_text, 22, COLOR_YELLOW, center=(hud_rect.width // 2, hud_rect.height // 2))

    _draw_lives(surface, lives, hud_rect)


def _draw_lives(surface, lives, hud_rect):
    """Desenha os 'corações' de vida como pequenos losangos neon, para não depender de um emoji de coração, que nem toda instalação de fonte do
    sistema consegue renderizar corretamente dentro do Pygame."""
    heart_size = 14
    spacing = 10
    total_width = lives * (heart_size + spacing)
    start_x = hud_rect.width - total_width - 24
    y = hud_rect.height // 2

    for i in range(lives):
        cx = start_x + i * (heart_size + spacing) + heart_size // 2
        points = [
            (cx, y - heart_size // 2),
            (cx + heart_size // 2, y),
            (cx, y + heart_size // 2),
            (cx - heart_size // 2, y),
        ]
        pygame.draw.polygon(surface, (255, 70, 90), points)
        pygame.draw.polygon(surface, (255, 180, 190), points, width=2)


def draw_play_area_border(surface, play_rect):
    """Moldura neon dupla ao redor da área jogável, para reforçar o visual
    de 'tela dentro de um gabinete de fliperama' de minha preferência."""
    pygame.draw.rect(surface, COLOR_NEON_BLUE, play_rect, width=4, border_radius=8)
    inner = play_rect.inflate(-14, -14)
    pygame.draw.rect(surface, (0, 120, 160), inner, width=1, border_radius=6)
