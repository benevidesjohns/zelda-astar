from queue import PriorityQueue


# Funcao Heuristica (Distancia de Manhattan)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Algoritmo A*
def algorithm(map, start_node, end_node):
    came_from = {}
    g_count = 0

    # Cria um dicionário, representando a lista aberta, e adiciona o node inicial
    open_list = {start_node}

    # Cria uma fila de prioridade (lista fechada) e adiciona o node inicial
    closed_list = PriorityQueue()
    closed_list.put((0, g_count, start_node))

    # Calcula o G Score para cada node
    g_score = {node: float("inf") for row in map.nodes for node in row}
    g_score[start_node] = 0

    # Calcula o F Score para cada node
    f_score = {node: float("inf") for row in map.nodes for node in row}
    f_score[start_node] = h(start_node.get_pos(), end_node.get_pos())

    # Executa o algoritmo enquanto a fila de prioridade nao estiver vazia
    while not closed_list.empty():

        # Pega o node com mais prioridade da lista fechada e o remove das duas listas
        current = closed_list.get()[2]
        open_list.remove(current)

        # Verifica se chegou no objetivo e constroi o caminho ate o mesmo
        if current == end_node:
            # Converte o dicionario came_from em uma lista
            came_from_list = [current]
            while current in came_from:
                current = came_from[current]
                came_from_list.append(current)

            # Retorna uma lista com o melhor caminho encontrado (do inicio para o final)
            return list(reversed(came_from_list))

        # Calcula o F, G e H dos vizinhos do node atual
        for neighbor in current.neighbors:
            temp_g = g_score[current] + neighbor.cost

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current

                # Define o F e G Scores para cada vizinho
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + \
                    h(neighbor.get_pos(), end_node.get_pos())

                # Veifica se o vizinho nao esta na lista aberta
                if neighbor not in open_list:
                    g_count += temp_g
                    closed_list.put((f_score[neighbor], g_count, neighbor))
                    open_list.add(neighbor)
