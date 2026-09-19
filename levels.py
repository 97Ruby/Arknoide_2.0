""" Responsável por transformar um número de fase (1 a 16) em uma lista de
objetos block posicionados na tela. Mantive essa lógica separada do
inicio do jogo para que adicionar/editar formatos de fase não exija tocar em
nada relacionado a colisão, pontuação ou input.

Cada "layout" é uma função que devolve uma matriz (lista de listas) de
0/1, onde 1 = tem bloco naquela célula do grid e 0 = célula vazia. A
função build_level() depois converte essa matriz em blocos de verdade,
já posicionados e coloridos por linha.

As 16 fases ciclam pelos 5 layouts que escolhi, aumentando o
número de linhas (mais blocos) a cada "volta" do ciclo, assim a fase 6
reaproveita o layout da fase 1, mas mais cheia/difícil. Motivos dessas escolhas? Simplesmente porque eu quis. :O"""

from entities.block import Block
from config import BLOCK_ROW_COLORS, BLOCK_ROW_POINTS

COLS = 12  # número de colunas usado por todos os layouts, para consistência visual


def _layout_classic(rows):
# Fileiras cheias, uma embaixo da outra, assim como o Arkanoid tradicional.
    return [[1] * COLS for _ in range(rows)]


def _layout_pyramid(rows):
    # Cada linha mais larga que a anterior, formando uma pirâmide centrada.
    grid = []
    for r in range(rows):
        filled = min(COLS, 2 * (r + 1))
        margin = (COLS - filled) // 2
        row = [0] * margin + [1] * filled + [0] * (COLS - filled - margin)
        grid.append(row)
    return grid


def _layout_side_walls(rows):
# Duas colunas verticais nas laterais, como em 'Paredes laterais'.
    grid = []
    for r in range(rows):
        row = [0] * COLS
        row[0] = row[1] = 1
        row[COLS - 1] = row[COLS - 2] = 1
        # Uma barreira horizontal periódica conectando as paredes, para não ficar só duas colunas soltas e vazias no meio. Mais bonito visualmente.
        if r % 3 == 0:
            row = [1] * COLS
        grid.append(row)
    return grid


def _layout_diamond(rows):
# Formato de losango/diamante centralizado
    grid = []
    half = rows // 2
    for r in range(rows):
        dist_from_center = abs(r - half)
        filled = max(2, COLS - dist_from_center * 2)
        filled = min(filled, COLS)
        margin = (COLS - filled) // 2
        row = [0] * margin + [1] * filled + [0] * (COLS - filled - margin)
        grid.append(row)
    return grid


def _layout_symbol(rows):
# Padrão inspirado em alien (symbol) de fliperama: um bloco central (cabeça) mais largo no topo e 'pernas' descendo nas laterais.
    base_pattern = [
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    ]
    # Repete/estende o padrão base verticalmente até atingir linhas.
    grid = []
    while len(grid) < rows:
        grid.extend(base_pattern)
    return grid[:rows]


# Ordem em que os layouts se repetem ao longo das 16 fases.
_LAYOUT_CYCLE = [_layout_classic, _layout_pyramid, _layout_side_walls, _layout_diamond, _layout_symbol]


def build_level(level_number, play_left, play_right, top_y):
    """Constrói a lista de blocos para a fase `level_number` (1-indexado).
    play_left/play_right: limites horizontais da área jogável em pixels (px).
    top_y: coordenada Y onde a primeira linha de blocos começa."""
    layout_fn = _LAYOUT_CYCLE[(level_number - 1) % len(_LAYOUT_CYCLE)]

    """" A cada "volta" completa pelo ciclo de layouts, aumenta uma linha 
    extra de blocos — assim a dificuldade cresce fase a fase mesmo 
    reaproveitando os mesmos desenhos. =P"""
    cycle_pass = (level_number - 1) // len(_LAYOUT_CYCLE)
    rows = min(len(BLOCK_ROW_COLORS) + cycle_pass, 10)

    grid = layout_fn(rows)

    play_width = play_right - play_left
    block_width = play_width / COLS
    block_height = 22
    spacing = 4

    blocks = []
    for row_index, row in enumerate(grid):
        # Cores/pontos ciclam pela paleta caso a fase tenha mais linhas que
        # cores cadastradas (grid maior que BLOCK_ROW_COLORS).
        color = BLOCK_ROW_COLORS[row_index % len(BLOCK_ROW_COLORS)]
        points = BLOCK_ROW_POINTS[row_index % len(BLOCK_ROW_POINTS)]

        for col_index, present in enumerate(row):
            if not present:
                continue
            x = play_left + col_index * block_width + spacing / 2
            y = top_y + row_index * (block_height + spacing)
            blocks.append(Block(x, y, block_width - spacing, block_height, color, points))

    return blocks


TOTAL_LEVELS = 16
