""" A bola se move sozinha, movimento automático, e
só muda de direção por colisões (paredes, barra, blocos) — o jogador nunca a controla diretamente. O "rastro" semitransparente simula o
efeito de brilho/cauda que eu quis reproduzir. """

import math
import random
import pygame
from config import BALL_RADIUS, BALL_BASE_SPEED, BALL_MAX_SPEED, BALL_SPEEDUP_PER_SECOND


class Ball:
    def __init__(self, x, y):
        self.radius = BALL_RADIUS
        self.x = x
        self.y = y
        self.speed = BALL_BASE_SPEED
        self.trail = []  # posições recentes, para desenhar o rastro

        # Ângulo inicial sempre "para cima" mas com componente horizontal
        # aleatória, para que cada partida/vida comece de forma um pouco
        # diferente (evita loops sempre idênticos de trajetória).
        angle = random.uniform(-0.6, 0.6) - math.pi / 2
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

    def reset(self, x, y):
        self.x, self.y = x, y
        self.speed = BALL_BASE_SPEED
        self.trail.clear()
        angle = random.uniform(-0.6, 0.6) - math.pi / 2
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

    def increase_speed_over_time(self, dt):
        """A dificuldade sobe conforme o tempo passa dentro da mesma fase. Usei um teto (BALL_MAX_SPEED) para a fase nunca
        ficar literalmente impossível. Pois no fundo eu sou boazinha siim!"""
        if self.speed < BALL_MAX_SPEED:
            self.speed = min(BALL_MAX_SPEED, self.speed + BALL_SPEEDUP_PER_SECOND * dt)

    def update(self, dt):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                            self.radius * 2, self.radius * 2)

    def bounce_horizontal(self):
        """Inverte a componente X da velocidade (bateu em parede lateral)."""
        self.dx *= -1

    def bounce_vertical(self):
        """Inverte a componente Y da velocidade (bateu no teto ou na barra)."""
        self.dy *= -1

    def bounce_off_paddle(self, paddle_rect):
        """ Regra de reflexo variável: o ponto de impacto na barra decide o ângulo de saída. Isso dá controle tático ao jogador (rebater na ponta manda a bola mais de lado) em vez de um rebote sempre
        simétrico, que tornaria o jogo repetitivo e menos justo com quem está jogando bem. """
        offset = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
        offset = max(-1, min(1, offset))  # trava entre -1 e 1

        max_angle = math.radians(65)  # ângulo máximo de saída em relação à vertical
        angle = offset * max_angle

        self.dx = math.sin(angle)
        self.dy = -abs(math.cos(angle))  # sempre para cima após bater na barra

    def draw(self, surface):
        # Rastro: círculos cada vez menores/mais fracos atrás da bola.
        for i, (tx, ty) in enumerate(self.trail):
            fade = i / len(self.trail)
            radius = max(1, int(self.radius * fade))
            color = (int(60 + 150 * fade), int(160 + 60 * fade), 255)
            pygame.draw.circle(surface, color, (int(tx), int(ty)), radius)

        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (150, 220, 255), (int(self.x), int(self.y)), self.radius, width=2)
