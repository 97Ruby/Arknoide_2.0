""" Camada fina sobre pygame.mixer. Adicionei musica no menu e na fase de gameplay, e efeitos sonoros que eu quis para testar a funcionalidade do som no jogo. Mas o usuario pode escolher/trocar as músicas e efeitos sonoros conforme desejar.
Nomes de arquivo esperados (ver sounds/README.txt para detalhes):
    menu_music.ogg / .mp3
    gameplay_music.ogg / .mp3
    hit_wall.wav
    hit_paddle.wav
    break_block.wav
    lose_life.wav
    game_over.wav
    victory.wav
    button_click.wav
"""

import os
import pygame
from config import SOUNDS_DIR

_SFX_CACHE = {}
_MIXER_OK = False


def init():
    """Inicializa o mixer uma única vez. Se o ambiente não tiver dispositivo de áudio disponível (comum em servidores/containers), o jogo continua funcionando normalmente, apenas sem som."""
    global _MIXER_OK
    try:
        pygame.mixer.init()
        _MIXER_OK = True
    except pygame.error:
        _MIXER_OK = False


def _find_file(name_without_ext):
    """Aceita tanto .ogg quanto .mp3/.wav para o mesmo nome lógico, para não forçar o usuário a converter o formato da música que ele já tem."""
    if not os.path.isdir(SOUNDS_DIR):
        return None
    for ext in (".ogg", ".mp3", ".wav"):
        candidate = os.path.join(SOUNDS_DIR, name_without_ext + ext)
        if os.path.isfile(candidate):
            return candidate
    return None


def play_music(name, loop=True):
    """Toca uma faixa de música em loop de fundo (menu ou fase)."""
    if not _MIXER_OK:
        return
    path = _find_file(name)
    if path is None:
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if loop else 0)
    except pygame.error:
        pass


def stop_music():
    if _MIXER_OK:
        pygame.mixer.music.stop()


def play_sfx(name, volume=0.7):
    """Toca um efeito sonoro curto (colisão, botão, etc.), com cache para não recarregar o .wav do disco a cada colisão."""
    if not _MIXER_OK:
        return
    if name not in _SFX_CACHE:
        path = _find_file(name)
        if path is None:
            _SFX_CACHE[name] = False  # marca como "não existe" para não tentar de novo
        else:
            try:
                _SFX_CACHE[name] = pygame.mixer.Sound(path)
            except pygame.error:
                _SFX_CACHE[name] = False

    sound = _SFX_CACHE[name]
    if sound:
        sound.set_volume(volume)
        sound.play()
