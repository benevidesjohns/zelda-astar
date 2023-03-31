from node import Node
from maps import hyrule, dungeon_1, dungeon_2, dungeon_3
from player import Player, make_start
from algorithm import algorithm
from itertools import permutations
import pygame


class Game:
    def __init__(self):
        self.current_start_point = (27, 24)
        self.current_end_point = None
        self.map = hyrule(self.current_start_point, None)
        self.node_size = 18
        self.window = None
        self.player = None
        self.state = 'hyrule'
        self.toggle_state = False
        self.started = False
        self.order_path = [],
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

        # Constroi o grid (matriz de nodes)
        self.map.set_nodes(self.make_grid(
            self.map, self.node_size
        ))

        # Define o ponto inicial do mapa e a posicao do jogador
        self.map.set_start_node()
        self.player = make_start(
            self.map.start_node.x, self.map.start_node.y
        )

        # Define o ponto final do mapa, caso esse seja estabelecido
        if self.map.end_point:
            self.map.set_end_node()

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
                self.map, self.map.get_node(
                    start), self.map.get_node(dungeons[i])
            )
            paths[f'dungeon_{i+1}_end'] = algorithm(
                self.map, self.map.get_node(
                    end), self.map.get_node(dungeons[i])
            )
            for j in range(i+1, len(dungeons)):
                paths[f'dungeon_{i+1}_dungeon_{j+1}'] = algorithm(
                    self.map, self.map.get_node(
                        dungeons[i]), self.map.get_node(dungeons[j])
                )
                paths[f'dungeon_{j+1}_dungeon_{i+1}'] = list(
                    reversed(paths[f'dungeon_{i+1}_dungeon_{j+1}']))

        # Calcula os custos para cada caminho
        costs = {}
        for key, nodes in paths.items():
            path_cost = sum(list(map(lambda node: node.terrain.cost, nodes)))
            costs[key] = path_cost - nodes[-1].terrain.cost

        # Lista todas as ordens de caminhos possíveis
        permuts = list(permutations(['dungeon_1', 'dungeon_2', 'dungeon_3']))
        orders = list(
            map(lambda order: ['start'] + list(order) + ['end'], permuts)
        )

        # Soma os custos para todas as ordens de caminhos possíveis
        order_paths = []
        best_cost = float("inf")
        best_order_path = 0

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
                best_order_path = index

        print('\n---------------------------------- MELHOR CAMINHO ------------------------------\n')
        print(order_paths[best_order_path])
        self.order_path = order_paths[best_order_path]['order']
        self.order_path.pop(0)
        self.map.end_point = self.current_end_point = self.points[self.order_path[0]]
        self.map.set_end_node()

        print('\n---------------------------------- OUTROS CAMINHOS ------------------------------\n')
        for i in range(len(order_paths)):
            if i != best_order_path:
                print(order_paths[i], end='\n\n')

    # Executa o algoritmo do astar
    def execute_algorithm(self):
        best_way = algorithm(self.map, self.map.start_node, self.map.end_node)

        # Constroi o melhor caminho encontrado
        self.reconstruct_path(
            best_way,
            list(reversed(best_way)),
            lambda: self.draw(
                self.window,
                self.width,
                self.map,
                self.node_size,
                self.player
            ),
            self.player,
        )

    # Atualiza os nodes que definem o caminho encontrado pelo algoritmo
    def reconstruct_path(self, path, reverse_path, draw, player_group):

        # Em Hyrule -> anda até a entrada da dungeon e entra
        if self.state == 'hyrule':

            # Percorre ate o ponto final
            for node in path:
                player = Player((node.x, node.y))
                player_group.empty()
                player_group.add(player)
                draw()

            # Entra na dungeon, caso o player nao tenha chegado ao objetivo final
            if self.order_path[0] != 'end':
                self.current_start_point = self.current_end_point
                self.toggle_state = True
                self.state = self.order_path.pop(0)

        # Nas Dungeons -> pega o pingente e volta para Hyrule
        else:

            # Vai até o pingente
            for node in path:
                player = Player((node.x, node.y))
                player_group.empty()
                player_group.add(player)
                draw()

            # Pega o pingente
            pygame.time.delay(200)

            # Volta para a entrada da dungeon
            for node in reverse_path:
                player = Player((node.x, node.y))
                player_group.empty()
                player_group.add(player)
                draw()

            # Sai da dungeon
            if self.order_path[0] == 'end':
                next_point = self.points['entrada_lost_woods']
            else:
                next_point = self.points[self.order_path[0]]

            self.current_end_point = next_point
            self.toggle_state = True
            self.state = 'hyrule'

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
            for local, coord in self.points.items():
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

    # TODO: Captura a posicao que o usuario clicou no grid
    def get_clicked_pos(self, pos, rows, size):
        gap = size // rows
        y, x = pos

        row = x // gap
        col = y // gap

        return row, col
