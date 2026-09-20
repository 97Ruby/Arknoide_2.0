""" Centraliza todas as constantes visuais e de jogabilidade.
Manter esses valores em um único lugar facilita ajustes de balanceamento
(velocidade, tamanhos) e de identidade visual (cores, tema neon) sem
precisar encontrar números "específicos" espalhados pelo código."""

import json
import os
import sys
""" Caminho do arquivo onde é salvo a resolução escolhida e progresso de fases (um arquivo JSON).
Fica ao lado do próprio jogo para funcionar em qualquer pasta que o usuário mova o projeto.
Quando empacotado com PyInstaller (--onefile), __file__ aponta para a pasta
temporária de extração (_MEIPASS), que é apagada ao fechar o programa — por isso o uso da 
pasta do .exe nesse caso, para o save persistir entre execuções."""

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
    # Dados empacotados via "datas" no .spec ficam em _MEIPASS (pasta _internal
    # no modo --onedir), que é diferente da pasta do .exe usada para o save.
    RESOURCES_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = BASE_DIR
SETTINGS_FILE = os.path.join(BASE_DIR, "save_data.json")
SOUNDS_DIR = os.path.join(RESOURCES_DIR, "musics")

# Resoluções disponíveis na tela de Configurações
# Escolha de resolução do jogo pelo usuário, para facilitar os ajustes de acordo com o tamanho da tela.
RESOLUTION_PRESETS = [
    (800, 600),
    (1024, 768),
    (1280, 720),
]
DEFAULT_RESOLUTION = RESOLUTION_PRESETS[1]

FPS = 60

# Paleta "Arcade Retrô" puramente preferencia estética de minha pessoa.
# Fundo espacial escuro com detalhes em azul neon brilhante.
COLOR_BG = (8, 8, 28)
COLOR_BG_STAR = (200, 210, 255)
COLOR_NEON_BLUE = (0, 200, 255)
COLOR_NEON_BLUE_DIM = (0, 90, 130)
COLOR_WHITE = (240, 245, 255)
COLOR_YELLOW = (255, 220, 40)
COLOR_RED_TITLE = (255, 90, 60)

# Cores das linhas de blocos, ordenadas de CIMA (mais pontos) para BAIXO (menos pontos), reproduzindo o gradiente arco-íris.
BLOCK_ROW_COLORS = [
    (230, 60, 60),    # vermelho   -> topo, vale mais
    (240, 120, 40),   # laranja
    (240, 210, 40),   # amarelo
    (70, 200, 90),    # verde
    (60, 140, 230),   # azul
    (150, 90, 220),   # roxo       -> mais embaixo, vale menos
]
# Pontuação correspondente a cada cor acima (mesmo índice = mesma linha).
BLOCK_ROW_POINTS = [60, 50, 40, 30, 20, 10]

# Jogabilidade
PADDLE_HEIGHT = 18
PADDLE_WIDTH_RATIO = 0.14      # largura da barra em relação à largura da tela
PADDLE_SPEED = 620             # pixels/segundo

BALL_RADIUS = 9
BALL_BASE_SPEED = 320          # velocidade inicial (pixels/segundo)
BALL_MAX_SPEED = 680           # trava para a bola não ficar impossível de rebater
BALL_SPEEDUP_PER_SECOND = 4.0  # o quanto a velocidade cresce por segundo

LIVES_START = 3                # número de vidas iniciais do jogador

# Área jogável: margens internas para caber a borda neon + HUD no topo.
PLAY_AREA_MARGIN = 24
HUD_HEIGHT = 64

GAME_TITLE = "ARKANOID 2.0"  # nome do jogo 


def load_save_data():
    """Carrega resolução escolhida e progresso de fases do disco.
    Se o arquivo não existir (primeira execução) ou estiver corrompido, devolve os valores padrão em vez de quebrar o jogo — preferi um save "zerado" a uma quebra na inicialização."""
    default = {
        "resolution": list(DEFAULT_RESOLUTION),
        "fullscreen": False,
        "max_unlocked_level": 1,
        "stars": {},  # ex: {"1": 1} -> fase 1 já foi concluída
    }
    if not os.path.exists(SETTINGS_FILE):
        return default
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        default.update(data)
        return default
    except (json.JSONDecodeError, OSError):
        return default


def save_save_data(data):
    """Persiste o progresso/configurações. Falha silenciosamente se o
    disco não for gravável — não é motivo para interromper a partida."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass
