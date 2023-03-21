from node import Node
from queue import PriorityQueue
from maps import hyrule, dungeon1, dungeon2, dungeon3
from player import Player, make_start
import pygame
import sys


class Game:
    def __init__(self):
        self.current_start_point = (27, 24)
        self.current_end_point = (32, 5)
        self.map = hyrule(self.current_start_point, self.current_end_point)
        self.node_size = 18
        self.window = None
        self.player = None
        self.state = 'hyrule'
        self.toggle_state = False
        self.dungeon_path = []

        # Constroi o mapa
        self.make_map(self.map)

    # Define as propriedades do mapa
    def make_map(self, map):
        self.map = map
        self.width = 504 if map.is_dungeon() else 756  # Tamanho da janela
        self.window = pygame.display.set_mode(
            (self.width, self.width))  # Janela
        self.map.set_nodes(self.make_grid(
            self.map, self.node_size))  # Define o grid
        self.map.set_start_end_nodes()  # Define os nodes iniciais e finais
        self.player = make_start(
            self.map.start_node.x, self.map.start_node.y)  # Define o jogador

    # Gerencia os estados (mapas) do jogo
    def state_manager(self):
        if self.state == 'hyrule' and self.toggle_state:
            self.make_map(
                hyrule(self.current_start_point, self.current_end_point))
            self.toggle_state = False

        if self.state == 'dungeon_1' and self.toggle_state:
            self.make_map(dungeon1())
            self.toggle_state = False

        if self.state == 'dungeon_2' and self.toggle_state:
            self.make_map(dungeon2())
            self.toggle_state = False

        if self.state == 'dungeon_3' and self.toggle_state:
            self.make_map(dungeon3())
            self.toggle_state = False

    def start(self):
        while True:

            # Gerencia os mapas
            self.state_manager()

            self.draw(self.window, self.width, self.map,
                      self.node_size, self.player)

            for event in pygame.event.get():

                # Verifica as teclas do teclado
                if event.type == pygame.KEYDOWN:

                    # SPACE - Inicia o jogo
                    if event.key == pygame.K_SPACE and self.map.start_node and self.map.end_node:
                        for row in self.map.nodes:
                            for node in row:
                                node.update_neighbors(self.map.nodes)

                        # Executa o algoritmo da astar
                        self.algorithm(
                            lambda: self.draw(
                                self.window,
                                self.width,
                                self.map,
                                self.node_size,
                                self.player
                            ),
                            self.map,
                            self.player
                        )

                    # R - Reinicia o jogo
                    if event.key == pygame.K_r:
                        self.player.empty()
                        self.map.start_node = None

                    # ESC - Encerra o jogo
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # Funcao Heuristica -> Distancia de Manhattan

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    # Atualiza os nodes que definem o caminho encontrado pelo algoritmo

    def reconstruct_path(self, path, reverse_path, draw, player_group, is_dungeon):
        # Percorre ate o ponto final
        for node in path:
            player = Player((node.x, node.y))
            player_group.empty()
            player_group.add(player)
            draw()

        # Entra na dungeon
        if self.state == 'hyrule':
            last_point = self.current_end_point

            for name, point in self.map.points.items():
                if point == last_point:
                    next_state = name
                    self.dungeon_path.append(name)
                    break

            self.current_start_point = self.current_end_point
            self.toggle_state = True
            self.state = next_state

        # Volta para o ponto inicial
        if is_dungeon:
            pygame.time.delay(200)  # Delay pra pegar o pingente
            for node in reverse_path:
                player = Player((node.x, node.y))
                player_group.empty()
                player_group.add(player)
                draw()

            # Sai da dungeon
            last_point = reverse_path[-1].get_pos()

            if len(self.dungeon_path) == 3:
                next_point = self.map.points['entrada_lost_woods']
            else:
                for name, point in self.map.points.items():
                    if 'dungeon' in name and not name in self.dungeon_path:
                        next_point = point

            if last_point == self.map.start_node.get_pos():
                self.current_end_point = next_point
                self.toggle_state = True
                self.state = 'hyrule'

                

    # Astar algorithm

    def algorithm(self, draw, map, player):
        came_from = {}
        g_count = 0

        # Cria uma fila de prioridade e adiciona o node inicial (lista fechada)
        closed_list = PriorityQueue()
        closed_list.put((0, g_count, map.start_node))

        open_list = {map.start_node}

        # Calcula o G Score para cada node
        g_score = {node: float("inf") for row in map.nodes for node in row}
        g_score[map.start_node] = 0

        # Calcula o F Score para cada node
        f_score = {node: float("inf") for row in map.nodes for node in row}
        f_score[map.start_node] = self.h(
            map.start_node.get_pos(), map.end_node.get_pos())

        # Executa enquanto a fila de prioridade nao estiver vazia
        while not closed_list.empty():

            # Verifica se deve sair do jogo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Pega o node com mais prioridade da lista fechada e o remove da lista aberta
            current = closed_list.get()[2]
            open_list.remove(current)

            # Verifica se chegou no objetivo e constroi o caminho ate o mesmo
            if current == map.end_node:

                # Convert came_from dict in a list
                came_from_list = [current]
                while current in came_from:
                    current = came_from[current]
                    came_from_list.append(current)

                # Reconstruct path between start and end points
                self.reconstruct_path(
                    reversed(came_from_list),
                    came_from_list,
                    draw,
                    player,
                    map.is_dungeon()
                )

                break

            # Calcula o F, G e H dos vizinhos do node atual
            for neighbor in current.neighbors:
                temp_g = g_score[current] + neighbor.terrain.cost

                if temp_g < g_score[neighbor]:
                    came_from[neighbor] = current

                    # Define o F e G Scores para cada vizinho
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + \
                        self.h(neighbor.get_pos(), map.end_node.get_pos())

                    # Veifica se o vizinho nao esta na lista aberta
                    if neighbor not in open_list:
                        g_count += temp_g
                        closed_list.put((f_score[neighbor], g_count, neighbor))
                        open_list.add(neighbor)

    # Constroi o grid (matriz) com os nodes definidos no mapa

    def make_grid(self, map, node_size):
        grid = []
        for i, row in enumerate(map.terrains):
            grid.append([])
            for j, terrain in enumerate(row):
                node = Node(i, j, node_size, terrain, map.size)
                grid[i].append(node)

        return grid

    # Desenha a grade

    def draw_grid(self, window, rows, width, node_size):
        for i in range(rows + 1):
            pygame.draw.line(
                window, (70, 70, 70),  (0, i *
                                        node_size), (width, i * node_size)
            )
            for j in range(rows):
                pygame.draw.line(
                    window, (70, 70, 70), (j * node_size,
                                           0), (j * node_size, width)
                )

    # Desenha na tela

    def draw(self, window, width, map, node_size, player):

        # Desenha os nodes na tela
        for row in map.nodes:
            for node in row:
                node.draw(window)

        # Desenha a grade que separa os nodes
        self.draw_grid(window, map.size, width, node_size)

        # Desenha as imagens no mapa de Hyrule
        if not map.is_dungeon():
            for local, coord in map.points.items():
                (x, y) = coord
                node = map.nodes[x][y]
                if 'dungeon' in local:
                    node.draw_image(window, 'entrada_dungeon')
                else:
                    node.draw_image(window, local)

        # Desenha as imagens no mapa da Dungeon
        else:
            map.start_node.draw_image(window, 'entrada_dungeon')
            map.end_node.draw_image(window, f'pingente_{map.name}')

        # Desenha o personagem
        player.draw(window)

        # Atualiza a tela
        pygame.display.update()
        pygame.time.delay(20)

    # Captura a posicao que o usuario clicou no grid

    def get_clicked_pos(self, pos, rows, size):
        gap = size // rows
        y, x = pos

        row = x // gap
        col = y // gap

        return row, col
