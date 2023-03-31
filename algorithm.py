from queue import PriorityQueue
import pygame
import sys


# Funcao Heuristica (Distancia de Manhattan)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Algoritmo A*
def algorithm(map):
    came_from = {}
    g_count = 0

    # Cria um dicionário, representando a lista aberta, e adiciona o node inicial
    open_list = {map.start_node}

    # Cria uma fila de prioridade (lista fechada) e adiciona o node inicial
    closed_list = PriorityQueue()
    closed_list.put((0, g_count, map.start_node))

    # Calcula o G Score para cada node
    g_score = {node: float("inf") for row in map.nodes for node in row}
    g_score[map.start_node] = 0

    # Calcula o F Score para cada node
    f_score = {node: float("inf") for row in map.nodes for node in row}
    f_score[map.start_node] = h(map.start_node.get_pos(), map.end_node.get_pos())

    # Executa o algoritmo enquanto a fila de prioridade nao estiver vazia
    while not closed_list.empty():

        # Verifica se deve sair do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pega o node com mais prioridade da lista fechada e o remove das duas listas
        current = closed_list.get()[2]
        open_list.remove(current)

        # Verifica se chegou no objetivo e constroi o caminho ate o mesmo
        if current == map.end_node:

            # Converte o dicionario came_from em uma lista
            came_from_list = [current]
            while current in came_from:
                current = came_from[current]
                came_from_list.append(current)

            # Retorna uma lista com o melhor caminho encontrado
            return came_from_list

        # Calcula o F, G e H dos vizinhos do node atual
        for neighbor in current.neighbors:
            temp_g = g_score[current] + neighbor.terrain.cost

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current

                # Define o F e G Scores para cada vizinho
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + \
                    h(neighbor.get_pos(), map.end_node.get_pos())

                # Veifica se o vizinho nao esta na lista aberta
                if neighbor not in open_list:
                    g_count += temp_g
                    closed_list.put((f_score[neighbor], g_count, neighbor))
                    open_list.add(neighbor)
