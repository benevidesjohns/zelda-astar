import pygame
from game import Game


if __name__ == '__main__':

    pygame.display.set_caption("Zelda A*")
    game = Game()
    game.start()

    # Define o mapa
    # map = hyrule()
    # map = dungeon1()
    # map = dungeon2()
    # map = dungeon3()

    # # Verifica o tamanho da janela do pygame (Hyrule -> 756, Dungeons -> 504)
    # width = 504 if map.is_dungeon() else 756

    # # Define a janela do pygame
    # window = pygame.display.set_mode((width, width))
    # pygame.display.set_caption("Zelda A*")

    # # Define o grid (matriz de nodes)
    # node_size = 18
    # grid = make_grid(map, node_size)
    # map.set_nodes(grid)

    # # Define os nodes inicial e final
    # map.set_start_end_nodes()
    # start = map.start_node
    # end = map.end_node

    # # Define o jogador
    # player_group = make_start(start.x, start.y)

    # # Inicia o jogo
    # while True:

    #     # Desenha o grid na tela
    #     draw(window, width, map, node_size, player_group)

    #     # Gerencia os eventos do pygame
    #     for event in pygame.event.get():

    #         # Encerra o jogo
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()

    #         # Seleciona o ponto de partida caso nao esteja setado
    #         if pygame.mouse.get_pressed()[0]:  # botao esquedo do mouse
    #             pos = pygame.mouse.get_pos()
    #             row, col = get_clicked_pos(pos, map.size, width)
    #             node = map.nodes[row][col]

    #             if not start:
    #                 start = node
    #                 player_group = make_start(node.x, node.y)

    #         # Verifica as teclas do teclado
    #         if event.type == pygame.KEYDOWN:

    #             # SPACE - Inicia o jogo
    #             if event.key == pygame.K_SPACE and start and end:
    #                 for row in map.nodes:
    #                     for node in row:
    #                         node.update_neighbors(map.nodes)

    #                 # Executa o algoritmo da astar
    #                 algorithm(
    #                     lambda: draw(window, width, map, node_size, player_group),
    #                     map.nodes,
    #                     start,
    #                     end,
    #                     player_group
    #                 )

    #             # R - Reinicia o jogo
    #             if event.key == pygame.K_r:
    #                 player_group.empty()
    #                 start = None

    #             # ESC - Encerra o jogo
    #             if event.key == pygame.K_ESCAPE:
    #                 pygame.quit()
    #                 sys.exit()
