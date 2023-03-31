from game import Game
import pygame
import sys

# TODO: Captura a posicao que o usuario clicou no grid
def get_clicked_pos(pos, rows, size):
    gap = size // rows
    y, x = pos

    row = x // gap
    col = y // gap

    return row, col


if __name__ == '__main__':

    game = Game(start_point=(20, 25))
    pygame.init()

    # Inicia o jogo
    while True:

        # Inicia o gerenciador de estados (mapas) do jogo
        game.state_manager()

        game.draw(game.window, game.width, game.map,
                  game.node_size, game.player)

        for event in pygame.event.get():

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # SPACE - Inicia o jogo
                if event.key == pygame.K_SPACE and game.map.start_node:
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

                #TODO: R - Reinicia o jogo
                if event.key == pygame.K_r:
                    game = Game(start_point=(20, 25))
                    game.current_start_point = None
                    game.map.start_node = None
                    game.started = False
                    game.finished = False

                # ESC - Encerra o jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            #TODO: Adicionar um novo ponto inicial, caso este não esteja definido
            if True:
                pass