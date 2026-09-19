""" Funções de desenho reutilizadas por várias telas (menu, jogo, game over...).
Isolar isso aqui evita duplicar código de "efeito neon" em cada estado. """

import random
import pygame

_FONT_CACHE = {}


def get_font(size, bold=True):
    """Cacheia fontes por tamanho para não recriar o objeto Font a cada frame. Usei uma fonte monoespaçada do sistema como
    substituta da fonte pixelada, o usuário pode trocar por
    uma .ttf retrô própria em `get_font` caso queira personalizar depois. Mas na minha ditadura apenas minhas escolhas valem!"""
    key = (size, bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont("couriernew,consolas,monospace", size, bold=bold)
    return _FONT_CACHE[key]


def draw_text(surface, text, size, color, center=None, topleft=None, bold=True):
    """ Renderiza texto e posiciona por centro ou canto superior esquerdo.
    Retorna o Rect final, útil para detectar clique em botões de texto."""
    font = get_font(size, bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    surface.blit(rendered, rect)
    return rect


def draw_glow_rect(surface, rect, color, glow_layers=4, border_radius=6):
    """ Simula o contorno neon "brilhante" desenhando várias
    bordas semitransparentes crescentes por baixo da borda sólida final.
    Uma superfície separada com alpha é necessária porque pygame.draw não
    suporta transparência direta em surfaces sem SRCALPHA. """
    glow_surface = pygame.Surface(
        (rect.width + glow_layers * 8, rect.height + glow_layers * 8), pygame.SRCALPHA
    )
    center = (glow_surface.get_width() // 2, glow_surface.get_height() // 2)
    for i in range(glow_layers, 0, -1):
        alpha = int(45 / i)
        layer_rect = pygame.Rect(0, 0, rect.width + i * 8, rect.height + i * 8)
        layer_rect.center = center
        pygame.draw.rect(glow_surface, (*color, alpha), layer_rect, border_radius=border_radius + i)
    surface.blit(glow_surface, (rect.centerx - glow_surface.get_width() // 2,
                                 rect.centery - glow_surface.get_height() // 2))
    pygame.draw.rect(surface, color, rect, width=3, border_radius=border_radius)


class Starfield:
    """ Fundo de estrelas estáticas com leve cintilação, para reforçar o tema espacial retro. Gerado uma vez e reaproveitado. """

    def __init__(self, width, height, count=90):
        self.stars = [
            [random.randint(0, width), random.randint(0, height), random.uniform(0.5, 2.2)]
            for _ in range(count)
        ]
        self.width = width
        self.height = height

    def resize(self, width, height):
        self.width = width
        self.height = height

    def draw(self, surface, color):
        # O brilho de cada estrela oscila com uma função senoidal do tempo,
        # criando cintilação sem custo de recalcular posições.
        t = pygame.time.get_ticks() / 500.0
        for i, (x, y, phase) in enumerate(self.stars):
            brightness = 0.5 + 0.5 * abs((t + phase) % 2 - 1)
            c = tuple(int(ch * brightness) for ch in color)
            pygame.draw.circle(surface, c, (x, y), 1)
