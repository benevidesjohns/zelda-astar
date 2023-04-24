from src.game import Game
from src.player import make_start
from src.utils import gif
import pygame
import sys

# Captura a posicao que o usuario clicou no grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    return x // gap, y // gap


if __name__ == '__main__':

    game = Game()

    while True:

        # Inicia o gerenciador de estados (mapas) do jogo
        game.state_manager()

        # Desenha os elementos da janela do jogo
        game.draw()

        # Gerencia os eventos do pygame
        for event in pygame.event.get():

            # MOUSE LEFT BUTTON - Define um ponto inicial, caso ainda não esteja
            if pygame.mouse.get_pressed()[0] and not game.map.start_node and game.state == 'hyrule':

                # Captura a posição na tela onde foi clicado com o mouse
                pos = pygame.mouse.get_pos()
                x, y = get_clicked_pos(pos, game.map.size, game.width)

                # Define o ponto inicial do mapa
                game.current_start_point = game.map.start_point = (x, y)
                game.map.set_start_node()
                game.player = make_start(game.map.start_node.get_coord())
                print(f'\nStart Point = ({x}, {y})')

                # Define a melhor ordem para passar pelas dungeons
                game.set_best_order()
                game.started = True

            # Executa ação do player ao trocar entre os mapas (dungeon/hyrule)
            if event.type == pygame.WINDOWFOCUSGAINED and game.started and not game.finished:
                game.start()

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # SPACE - Inicia o jogo
                if event.key == pygame.K_SPACE and game.started and not game.running and not game.finished:
                    game.start()
                    game.running = True

                # R - Reinicia o jogo
                if event.key == pygame.K_r:
                    game = Game()

                # ESC - Encerra o jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Exibe um gif quando o link chegar na master sword
            if game.finished:
                pygame.display.quit()
                pygame.display.init()
                gif.run('assets/img/skyward-sword-zelda.gif')
