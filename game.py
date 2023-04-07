from node import Node
from maps import hyrule, dungeon_1, dungeon_2, dungeon_3
from player import Player, make_start
from algorithm import algorithm
from itertools import permutations
import pygame


class Game:
    def __init__(self, start_point=None):
        self.current_start_point = start_point
        self.current_end_point = None
        self.current_path = None
        self.path = None
        self.map = hyrule(self.current_start_point, None)
        self.nodes_group = pygame.sprite.Group()
        self.node_size = 18
        self.window = None
        self.player = None
        self.state = 'hyrule'
        self.toggle_state = False
        self.started = False
        self.running = False
        self.finished = False
        self.total_cost = 0,
        self.order = [],
        self.points = {
            'dungeon_1': (32, 5),
            'dungeon_2': (1, 24),
            'dungeon_3': (17, 39),
            'master_sword': (1, 2),
            'entrada_lost_woods': (5, 6)
        }

        self.make_map(self.map)

    # Define as propriedades do mapa
    def make_map(self, map):
        self.map = map

        # Constroi o grid (matriz de nodes)
        self.map.set_nodes(self.make_grid())

        # Define os vizinhos de cada node
        for row in self.map.nodes:
            for node in row:
                node.update_neighbors(self.map.nodes)

        # Define o ponto inicial do mapa e a posicao do jogador
        if self.map.start_point:
            self.map.set_start_node()
            self.player = make_start(
                self.map.start_node.x, self.map.start_node.y
            )

        # Define o ponto final do mapa, caso esse seja estabelecido
        if self.map.end_point:
            self.map.set_end_node()

        # Define a janela e o seu tamanho
        pygame.display.quit()
        pygame.display.init()

        if self.map.is_dungeon():
            pygame.display.set_caption(
                f'Zelda Astar - {" ".join(self.map.name.capitalize().split("_"))}'
            )
            self.width = 504
        else:
            pygame.display.set_caption(
                f'Zelda Astar - {self.map.name.capitalize()}'
            )
            self.width = 756

        self.window = pygame.display.set_mode((self.width, self.width))

        # Define o próximo caminho a seguir no mapa de hyrule
        if self.started and self.state == 'hyrule':
            self.current_path = self.path.pop(0)

    # Gerencia os estados (mapas) do jogo
    def state_manager(self):
        if self.state == 'hyrule' and self.toggle_state:
            self.make_map(
                hyrule(self.current_start_point, self.current_end_point)
            )
            self.toggle_state = False

        if self.state == 'dungeon_1' and self.toggle_state:
            self.make_map(dungeon_1())
            self.toggle_state = False

        if self.state == 'dungeon_2' and self.toggle_state:
            self.make_map(dungeon_2())
            self.toggle_state = False

        if self.state == 'dungeon_3' and self.toggle_state:
            self.make_map(dungeon_3())
            self.toggle_state = False

    # Define a melhor ordem para passar pelas dungeons
    def set_best_order(self):
        start = self.current_start_point
        dungeons = [
            self.points['dungeon_1'],
            self.points['dungeon_2'],
            self.points['dungeon_3']
        ]
        end = self.points['entrada_lost_woods']

        # Obtem o melhor caminho entre cada dungeon e os pontos final e inicial
        paths = {}
        for i in range(len(dungeons)):
            paths[f'start_dungeon_{i+1}'] = algorithm(
                self.map, self.map.get_node(start),
                self.map.get_node(dungeons[i])
            )
            paths[f'dungeon_{i+1}_entrada_lost_woods'] = algorithm(
                self.map, self.map.get_node(dungeons[i]),
                self.map.get_node(end)
            )
            for j in range(i+1, len(dungeons)):
                paths[f'dungeon_{i+1}_dungeon_{j+1}'] = algorithm(
                    self.map, self.map.get_node(dungeons[i]),
                    self.map.get_node(dungeons[j])
                )
                paths[f'dungeon_{j+1}_dungeon_{i+1}'] = list(
                    reversed(paths[f'dungeon_{i+1}_dungeon_{j+1}'])
                )

        # Calcula os custos para cada caminho
        costs = {}
        for key, nodes in paths.items():
            path_cost = sum(list(map(lambda node: node.cost, nodes)))
            costs[key] = path_cost - nodes[-1].cost

        # Lista todas as ordens de caminhos possíveis
        permuts = list(permutations(['dungeon_1', 'dungeon_2', 'dungeon_3']))
        orders = list(
            map(lambda order: ['start'] + list(order) + ['entrada_lost_woods'], permuts)
        )

        # Soma os custos para todas as ordens de caminhos possíveis
        # e verifica a melhor ordem de caminho entre as dungeons
        order_paths = []
        best_cost = float("inf")
        best_order_path_index = 0

        for index, order in enumerate(orders):
            total_cost = 0

            for i in range(len(order)-1):
                total_cost += costs[f'{order[i]}_{order[i+1]}']

            order_paths.append({
                'total_cost': total_cost,
                'order': order
            })

            if total_cost < best_cost:
                best_cost = total_cost
                best_order_path_index = index

        print('\n------------------------ MELHOR CAMINHO ENTRE AS DUNGEONS -----------------------\n')
        print(order_paths[best_order_path_index])

        # Seleciona os paths da melhor ordem de caminho entre as dungeons
        best_order_path = order_paths[best_order_path_index]['order']
        best_paths = []
        for i in range(len(best_order_path)-1):
            best_paths.append(paths[f'{best_order_path[i]}_{best_order_path[i+1]}'])

        # Define o order path e o primeiro end point do mapa
        self.path = best_paths
        self.current_path = self.path.pop(0)

        self.order = order_paths[best_order_path_index]['order']
        self.order.pop(0)

        self.map.end_point = self.current_end_point = self.points[self.order[0]]
        self.map.set_end_node()

        print('\n-------------------------------- OUTROS CAMINHOS --------------------------------\n')
        for i in range(len(order_paths)):
            if i != best_order_path_index:
                print(order_paths[i], end='\n\n')

    # Inicia o jogo
    def start(self):
        if self.state == 'hyrule':
            self.reconstruct_path(self.current_path, list(reversed(self.current_path)))
        else:
            best_way = algorithm(self.map, self.map.start_node, self.map.end_node)
            self.reconstruct_path(best_way, list(reversed(best_way)))

    # Faz a animacao do player andando no mapa
    def draw_player(self, path, delay):

        for node in path:

            # Desenha o player
            player = Player((node.x, node.y))
            self.player.add(player)
            self.player.draw(self.window)
            pygame.display.update()
            pygame.time.delay(delay)

            # Remove o player
            if node != path[-1]:
                self.player.add(node)
                self.player.draw(self.window)
                self.player.empty()

            # Redesenha a grade
            if self.state == 'hyrule':
                self.draw_grid()

            # Redesenha os artifacts
            if not node.artifact is None and 'pingente' not in node.artifact_name:
                node.artifact.draw(self.window)

            pygame.display.update()

    # Atualiza os nodes que definem o caminho encontrado pelo algoritmo
    def reconstruct_path(self, path, reverse_path):

        # Em Hyrule -> anda até a entrada da dungeon e entra
        if self.state == 'hyrule':

            # Percorre ate o ponto final
            self.draw_player(path=path, delay=20)

            # Entra na dungeon, caso o player nao tenha chegado ao objetivo final
            if self.order[0] != 'entrada_lost_woods':
                self.current_start_point = self.current_end_point
                self.toggle_state = True
                self.state = self.order.pop(0)

            # Chega a entrada de lost woods (caminhando lentamente e com estilo)
            else:
                self.map.start_point = self.current_end_point
                self.map.end_point = self.points['master_sword']
                self.map.set_start_node()
                self.map.set_end_node()

                final_path = algorithm(
                    self.map, self.map.start_node, self.map.end_node)

                pygame.time.delay(500)  # Pausa dramática
                self.draw_player(path=final_path, delay=200)
                self.finished = True

        # Nas Dungeons -> pega o pingente e volta para Hyrule
        else:
            # Vai até o pingente
            self.draw_player(path=path, delay=20)
            pygame.time.delay(200)

            # Volta para a entrada da dungeon
            self.draw_player(path=reverse_path, delay=20)

            # Sai da dungeon
            self.current_end_point = self.points[self.order[0]]
            self.toggle_state = True
            self.state = 'hyrule'

   # Constroi o grid (matriz) com os nodes definidos no mapa
    def make_grid(self):
        grid = []
        for i, row in enumerate(self.map.terrains):
            grid.append([])
            for j, terrain in enumerate(row):
                node = Node(i, j, self.node_size, terrain, self.map.size)
                self.nodes_group.add(node)
                grid[i].append(node)

        return grid

    # Desenha a grade
    def draw_grid(self):
        for i in range(self.map.size + 1):
            pygame.draw.line(
                self.window, (70, 70, 70), (0, i * self.node_size),
                (self.width, i * self.node_size)
            )
            for j in range(self.map.size):
                pygame.draw.line(
                    self.window, (70, 70, 70), (j * self.node_size, 0),
                    (j * self.node_size, self.width)
                )

    # Desenha na tela
    def draw(self, delay=10):
        # Desenha os nodes na tela
        self.nodes_group.draw(self.window)

        # Desenha a grade que separa os nodes
        if self.state == 'hyrule':
            self.draw_grid()

        # Desenha as imagens no mapa de Hyrule
        if not self.map.is_dungeon():
            for local, coord in self.points.items():
                (x, y) = coord
                node = self.map.nodes[x][y]
                if 'dungeon' in local:
                    node.set_artifact('entrada_dungeon')
                else:
                    node.set_artifact(local)

                node.artifact.draw(self.window)

        # Desenha as imagens no mapa da Dungeon
        else:
            self.map.start_node.set_artifact('entrada_dungeon')
            self.map.start_node.artifact.draw(self.window)
            self.map.end_node.set_artifact(f'pingente_{self.map.name}')
            self.map.end_node.artifact.draw(self.window)

        # Desenha o personagem
        if self.player:
            self.player.draw(self.window)

        # Atualiza a tela
        pygame.display.update()
        pygame.time.delay(delay)
