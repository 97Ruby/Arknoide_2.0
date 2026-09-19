""" Define a interface comum a todas as "telas" do jogo (Menu, Seleção de Fase,
Configurações, Jogo, Game Over, Vitória). Usar um padrão de "máquina de estados" com uma interface fixa (handle_event/update/draw) é o que permite ao main.py trocar de tela sem precisar saber os detalhes de cada uma, ele só chama esses três métodos no estado que estiver ativo no momento. """


class BaseState:
    def __init__(self, app):
        self.app = app  # referência ao objeto App (main.py), dá acesso a screen, config, trocar de estado etc.

    def on_enter(self):
        """Chamado toda vez que este estado se torna o estado ativo.
        Serve para resetar coisas como música de fundo ou temporizadores."""
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
