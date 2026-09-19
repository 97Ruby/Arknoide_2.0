""" Um bloco individual do cenário. Guardei os pontos que ele vale junto com a cor (em vez de calcular pontos "pela posição na tela" depois), porque isso deixa a regra de pontuação por linha explícita e fácil de conferir. """

import pygame


class Block:
    def __init__(self, x, y, width, height, color, points):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.points = points
        self.alive = True  # vira False quando atingido.

    def draw(self, surface):
        if not self.alive:
            return
        # Corpo sólido + uma faixa mais clara no topo para dar efeito
        # "brilhante/gel" parecido com os blocos da imagem de referência,
        # e uma borda escura para separar visualmente um bloco do outro.
        pygame.draw.rect(surface, self.color, self.rect, border_radius=3)

        highlight = tuple(min(255, c + 60) for c in self.color)
        highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height // 3)
        pygame.draw.rect(surface, highlight, highlight_rect, border_radius=2)

        shadow = tuple(max(0, c - 70) for c in self.color)
        pygame.draw.rect(surface, shadow, self.rect, width=2, border_radius=3)
