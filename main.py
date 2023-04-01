from game import Game
from player import make_start
import pygame
import sys

# TODO: Captura a posicao que o usuario clicou no grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = x // gap
    col = y // gap

    return row, col

if __name__ == '__main__':

    game = Game()
    pygame.init()

    # Inicia o jogo
    while True:

        # Inicia o gerenciador de estados (mapas) do jogo
        game.state_manager()

        game.draw(game.window, game.width, game.map,
                  game.node_size, game.player)

        for event in pygame.event.get():

            # Adicionar um novo ponto inicial, caso este não esteja definido
            if pygame.mouse.get_pressed()[0] and not game.map.start_node:
                pos = pygame.mouse.get_pos()
                y, x = get_clicked_pos(pos, game.map.size, game.width)
                game.current_start_point = (y, x)
                game.map.start_point = (y, x)
                game.make_map(game.map)

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # SPACE - Inicia o jogo
                if event.key == pygame.K_SPACE and game.current_start_point:
                    for row in game.map.nodes:
                        for node in row:
                            node.update_neighbors(game.map.nodes)

                    # Define a melhor ordem para passar pelas dungeons
                    if not game.started:
                        game.set_best_order()
                        game.started = True

                    # Executa o algoritmo do astar
                    if game.started and not game.finished:
                        game.execute_algorithm()

                # TODO: R - Reinicia o jogo
                if event.key == pygame.K_r:
                    game = Game()
                    game.current_start_point = None
                    game.map.start_node = None
                    game.started = False
                    game.finished = False

                # ESC - Encerra o jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
