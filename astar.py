from node import Node
from queue import PriorityQueue
import maps as mp
import pygame
import sys
import time

# Definicoes da janela do pygame
WINDOW_SIZE = 840
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Zelda A*")

# Cores da janela do pygame
LINE_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (255, 255, 255)

# Funcao da Heuristica -> Distancia de Manhattan
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Atualiza os nodes que definem o caminho encontrado pelo algoritmo
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


# Astar algorithm
def algorithm(draw, grid, start, end, slowmode):
    came_from = {}
    g_count = 0

    # Cria uma fila de prioridade e adiciona o node inicial (lista fechada)
    closed_list = PriorityQueue()
    closed_list.put((0, g_count, start))

    open_list = {start}

    # Calcula o G Score para cada node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # Calcula o F Score para cada node
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # Executa enquanto a fila de prioridade nao estiver vazia
    while not closed_list.empty():
        if slowmode:
            time.sleep(1)

        # Verifica se deve sair do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Pega o node com mais prioridade da fila e remove o mesmo do set
        current = closed_list.get()[2]
        open_list.remove(current)

        # Verifica se chegou no objetivo e exibe o caminho ate o mesmo
        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.terrain.cost

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current

                # Define o G Score e o F Score para cada vizinho
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                # Veifica se o vizinho nao esta na lista aberta
                if neighbor not in open_list:
                    g_count += temp_g_score
                    closed_list.put((f_score[neighbor], g_count, neighbor))
                    open_list.add(neighbor)

    return False


# Constroi o grid (matriz) com os nodes definidos no mapa
def make_grid(window_size, map):
    grid = []
    gap = window_size // map.size
    for i, row in enumerate(map.terrains):
        grid.append([])
        for j, terrain in enumerate(row):
            node = Node(i, j, gap, terrain, map.size)
            grid[i].append(node)
    
    return grid


# Desenha a grade
def draw_grid(window, rows, window_size):
    gap = window_size // rows
    for i in range(rows):
        pygame.draw.line(window, LINE_COLOR, (0, i * gap), (window_size, i * gap))
        for j in range(rows):
            pygame.draw.line(window, LINE_COLOR, (j * gap, 0), (j * gap, window_size))


# Desenha na tela
def draw(window, grid, rows, size):
    window.fill(BACKGROUND_COLOR)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, size)
    pygame.display.update()


# Captura a posicao que o usuario clicou no grid
def get_clicked_pos(pos, rows, size):
    gap = size // rows
    y, x = pos

    row = x // gap
    col = y // gap

    return row, col


# Funcao principal
def main(window, size, slowmode):
    # map_dungeon = mp.dungeon1()
    # map_dungeon = mp.dungeon2()
    map_dungeon = mp.dungeon3()
    grid = make_grid(size, map_dungeon)

    # Ponto inicial e final do mapa
    start_point = map_dungeon.start_point
    end_point = map_dungeon.end_point

    # Nodes referentes aos pontos inicial e final do mapa
    start = grid[start_point[0]][start_point[1]]
    end = grid[end_point[0]][end_point[1]]

    start.make_start()
    end.make_end()

    run = True
    while run:

        # Desenha o grid na tela
        draw(window, grid, map_dungeon.size, size)

        # Gerencia os eventos do pygame
        for event in pygame.event.get():

            # Encerra o jogo
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, map_dungeon.size, size)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # Inicia o jogo ao pressionar a tecla SPACE
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Executa o algoritmo da astar
                    algorithm(
                        lambda: draw(window, grid, map_dungeon.size, size),
                        grid,
                        start,
                        end,
                        slowmode
                    )

                # Reinicia o jogo ao pressionar a tecla R
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(size, map_dungeon)

    # Encerra o jogo
    pygame.quit()


if __name__ == '__main__':

    # Set slow mode
    slowmode = False
    if len(sys.argv) > 1:
        slowmode = True

    main(WINDOW, WINDOW_SIZE, slowmode)
