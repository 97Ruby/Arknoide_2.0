""" O coração do jogo: aqui tem a barra, a bola, os blocos da fase atual e todas as regras de colisão/pontuação/vidas. Mantive essa lógica em um só lugar (em vez de espalhar física entre várias classes) porque colisão em Arkanoid depende de conhecer todo os elementos ao mesmo tempo (bola x
barra, bola x parede, bola x cada bloco), então centralizar aqui evita dependências circulares entre entidades. """

import pygame
from states.base_state import BaseState
from entities.paddle import Paddle
from entities.ball import Ball
from levels import build_level
from ui import draw_hud, draw_play_area_border
from utils import draw_text
from config import PLAY_AREA_MARGIN, HUD_HEIGHT, LIVES_START, GAME_TITLE
import sound_manager


class GameState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.level_number = 1
        self.score = 0
        self.lives = LIVES_START
        self.paused = False
        self._recompute_play_area()

    def _recompute_play_area(self):
        """ Define o retângulo jogável com base no tamanho atual da janela. Recalculado sempre que o jogo é reiniciado, pois a resolução pode ter sido trocada na tela de Configurações """
        w, h = self.app.screen.get_size()
        self.hud_rect = pygame.Rect(0, 0, w, HUD_HEIGHT)
        self.play_rect = pygame.Rect(
            PLAY_AREA_MARGIN,
            HUD_HEIGHT + PLAY_AREA_MARGIN,
            w - PLAY_AREA_MARGIN * 2,
            h - HUD_HEIGHT - PLAY_AREA_MARGIN * 2,
        )

    def start_level(self, level_number):
        """ Prepara uma nova fase do zero (chamado ao entrar no jogo e ao avançar de fase). Diferente de resetar após perder uma vida. """
        self._recompute_play_area()
        self.level_number = level_number
        self.lives = LIVES_START
        self.score = 0
        self.elapsed_in_level = 0.0
        self.paused = False
        self._spawn_paddle_and_ball()
        self.blocks = build_level(
            level_number, self.play_rect.left + 4, self.play_rect.right - 4, self.play_rect.top + 30
        )
        sound_manager.play_music("gameplay_music")

    def _spawn_paddle_and_ball(self):
        self.paddle = Paddle(*self.app.screen.get_size(), self.play_rect.left, self.play_rect.right)
        ball_x = self.paddle.rect.centerx
        ball_y = self.paddle.rect.top - 12
        self.ball = Ball(ball_x, ball_y)
        self.ball_launched = False  # a bola espera um clique antes de sair

    def on_enter(self):
        # on_enter é chamado pelo App sempre que este estado volta a ficar
        # ativo; a criação real da fase acontece em start_level(), disparada
        # explicitamente pelo menu/seleção de fase (ver app.start_level).
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_state("menu")
            elif event.key == pygame.K_p:
                self.paused = not self.paused
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.ball_launched:
            # A bola só começa a se mover sozinha depois desse primeiro
            # clique, dá um instante para o jogador se posicionar antes do
            # movimento automático começar.
            self.ball_launched = True

    def update(self, dt):
        if self.paused:
            return

        keys = pygame.key.get_pressed()
        self.paddle.handle_input(dt, keys)

        if not self.ball_launched:
            # Bola fixa na barra até o lançamento inicial (clique do mouse). 
            self.ball.x = self.paddle.rect.centerx
            self.ball.y = self.paddle.rect.top - self.ball.radius - 2
            return

        self.elapsed_in_level += dt
        self.ball.increase_speed_over_time(dt)
        self.ball.update(dt)
        self._handle_wall_collisions()
        self._handle_paddle_collision()
        self._handle_block_collisions()
        self._check_ball_lost()

    # Colisões

    def _handle_wall_collisions(self):
        ball_rect = self.ball.get_rect()
        if ball_rect.left <= self.play_rect.left or ball_rect.right >= self.play_rect.right:
            self.ball.bounce_horizontal()
            # Reposiciona para dentro da área, evitando que a bola "grude"
            # na parede oscilando quando o dt é maior em quedas de FPS.
            self.ball.x = max(self.play_rect.left + self.ball.radius,
                               min(self.ball.x, self.play_rect.right - self.ball.radius))
            sound_manager.play_sfx("hit_wall")

        if ball_rect.top <= self.play_rect.top + 26:  # 26 = espaço reservado à borda superior
            self.ball.bounce_vertical()
            self.ball.y = self.play_rect.top + 26 + self.ball.radius
            sound_manager.play_sfx("hit_wall")

    def _handle_paddle_collision(self):
        ball_rect = self.ball.get_rect()
        if ball_rect.colliderect(self.paddle.rect) and self.ball.dy > 0:
            self.ball.bounce_off_paddle(self.paddle.rect)
            self.ball.y = self.paddle.rect.top - self.ball.radius - 1
            sound_manager.play_sfx("hit_paddle")

    def _handle_block_collisions(self):
        ball_rect = self.ball.get_rect()
        for block in self.blocks:
            if not block.alive:
                continue
            if not ball_rect.colliderect(block.rect):
                continue

            block.alive = False
            self.score += block.points
            sound_manager.play_sfx("break_block")

            # Decide se o rebote deve ser horizontal ou vertical comparando
            # a sobreposição em X vs. em Y, é uma aproximação simples e
            # robusta o suficiente para blocos retangulares alinhados a
            # uma grade, sem precisar de física de colisão contínua. Confia pai!
            overlap_x = min(ball_rect.right, block.rect.right) - max(ball_rect.left, block.rect.left)
            overlap_y = min(ball_rect.bottom, block.rect.bottom) - max(ball_rect.top, block.rect.top)
            if overlap_x < overlap_y:
                self.ball.bounce_horizontal()
            else:
                self.ball.bounce_vertical()
            break  # só um bloco é destruído por colisão, mesmo se dois se sobrepuserem na borda

        if all(not b.alive for b in self.blocks):
            self._win_level()

    def _check_ball_lost(self):
        if self.ball.y - self.ball.radius > self.play_rect.bottom:
            self.lives -= 1
            sound_manager.play_sfx("lose_life")
            if self.lives <= 0:
                self._game_over()
            else:
                self._spawn_paddle_and_ball()

    # Transições

    def _game_over(self):
        sound_manager.stop_music()
        sound_manager.play_sfx("game_over")
        self.app.change_state("game_over", score=self.score, level_number=self.level_number)

    def _win_level(self):
        sound_manager.stop_music()
        sound_manager.play_sfx("victory")
        self.app.unlock_next_level(self.level_number)
        self.app.change_state("victory", score=self.score, level_number=self.level_number)

    # Desenho

    def draw(self, surface):
        surface.fill((6, 6, 22))
        self.app.starfield.draw(surface, (200, 210, 255))

        draw_play_area_border(surface, self.play_rect)
        for block in self.blocks:
            block.draw(surface)

        self.paddle.draw(surface)
        self.ball.draw(surface)

        draw_hud(surface, self.score, self.level_number, self.lives, self.hud_rect)

        if not self.ball_launched:
            draw_text(surface, "Clique para lançar a bola", 18, (220, 220, 230),
                      center=(self.play_rect.centerx, self.play_rect.centery))

        if self.paused:
            draw_text(surface, "PAUSADO (P para continuar)", 28, (255, 255, 255),
                      center=(self.play_rect.centerx, self.play_rect.centery))
