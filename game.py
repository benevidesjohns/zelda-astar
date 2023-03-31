from node import Node
from maps import hyrule, dungeon_1, dungeon_2, dungeon_3
from player import Player, make_start
from algorithm import algorithm
import pygame


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
                f'Zelda Astar - {self.map.name.capitalize()}')
            self.width = 756

        self.window = pygame.display.set_mode((self.width, self.width))

        # Constroi o grid (matriz de nodes)
        self.map.set_nodes(self.make_grid(
            self.map, self.node_size)
        )

        # Define os pontos inicial e final do mapa e a posicao do jogador
        self.map.set_start_end_nodes()
        self.player = make_start(
            self.map.start_node.x, self.map.start_node.y
        )

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

    # Executa o algoritmo do astar
    def execute_algorithm(self):
        best_way = algorithm(self.map)

        # Constroi o melhor caminho encontrado
        self.reconstruct_path(
            reversed(best_way),
            best_way,
            lambda: self.draw(
                self.window,
                self.width,
                self.map,
                self.node_size,
                self.player
            ),
            self.player,
            self.map.is_dungeon()
        )

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
