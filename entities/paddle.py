""" A barra que o jogador controla. Fica isolada em sua própria classe, assim a lógica de movimento/desenho não se mistura com a lógica de colisão do GameState, facilitando leitura e testes futuros.  """

import pygame
from config import PADDLE_HEIGHT, PADDLE_SPEED


class Paddle:
    def __init__(self, screen_width, screen_height, play_left, play_right):
        self.screen_width = screen_width
        self.width = int(screen_width * 0.14)
        self.height = PADDLE_HEIGHT
        self.play_left = play_left    # limite esquerdo da área jogável
        self.play_right = play_right  # limite direito da área jogável

        # Começa centralizada, perto do fundo da área jogável.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = (play_left + play_right) // 2
        self.rect.bottom = screen_height - 40

    def handle_input(self, dt, keys):
        """Move a barra conforme as teclas pressionadas. Usei o dt (tempo decorrido desde o último frame) multiplicando a velocidade para que o movimento seja consistente independente do FPS real da máquina do usuário. """
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1

        self.rect.x += int(direction * PADDLE_SPEED * dt)

        # Trava a barra dentro da área jogável (não deixa "vazar" pela borda neon).
        if self.rect.left < self.play_left:
            self.rect.left = self.play_left
        if self.rect.right > self.play_right:
            self.rect.right = self.play_right

    def reset_position(self):
        self.rect.centerx = (self.play_left + self.play_right) // 2

    def draw(self, surface):
        # Corpo em gradiente vermelho->laranja para lembrar a barra da imagem,
        # desenhado em fatias verticais finas (gradiente manual, sem depender
        # de bibliotecas extras).
        for i in range(self.rect.width):
            t = i / max(1, self.rect.width - 1)
            r = int(200 + 55 * t)
            g = int(60 + 40 * t)
            b = 40
            pygame.draw.line(
                surface, (r, g, b),
                (self.rect.left + i, self.rect.top),
                (self.rect.left + i, self.rect.bottom),
            )
        # Contorno neon fino por cima para casar com o tema arcade.
        pygame.draw.rect(surface, (0, 200, 255), self.rect, width=2, border_radius=4)
