from game import Game
from player import make_start
import pygame
import gif
import sys


# Captura a posicao que o usuario clicou no grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = x // gap
    col = y // gap

    return row, col


if __name__ == '__main__':

    game = Game()
    pygame.init()

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
                y, x = get_clicked_pos(pos, game.map.size, game.width)

                # Define o ponto inicial do mapa
                game.current_start_point = game.map.start_point = (y, x)
                game.map.set_start_node()
                game.player = make_start(
                    game.map.start_node.x, game.map.start_node.y
                )

                # Define a melhor ordem para passar pelas dungeons
                game.set_best_order()
                game.started = True

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # SPACE - Inicia o jogo
                if event.key == pygame.K_SPACE and game.started and not game.running and not game.finished:
                    game.start()
                    # game.running = True

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
                gif.run('img/skyward-sword-zelda.gif')
