import pygame

from .template.maps import hyrule, dungeon_1, dungeon_2, dungeon_3
from .player import make_start, move
from .utils.algorithm import algorithm
from .utils.mixer import Mixer
from .utils.outlined_font import render
from .utils.constants import CPG11, BLACK, RED, GRAY, NODE_SIZE


class Game:
    def __init__(self, start_point=None):

        # Janela do pygame
        self.window = None

        # Gerencia os mapas do jogo
        self.state = 'hyrule'
        self.toggle_state = False

        # Verificações do estado atual do jogo (started, running e finished)
        self.started = False
        self.running = False
        self.finished = False

        # Pontos de referência
        self.current_start_point = start_point
        self.current_end_point = None
        self.points = {
            'dungeon_1': (1, 24),
            'dungeon_2': (17, 39),
            'dungeon_3': (32, 5),
            'master_sword': (1, 2),
            'entrada_lost_woods': (5, 6)
        }

        # Caminhos nos mapas
        self.map = hyrule(self.current_start_point, None)
        self.order = [],
        self.current_order = None
        self.path = None
        self.current_path = None
        self.costs = {}
        self.total_cost = int(0)
        self.best_order = []

        # Nodes (elementos do mapa)
        self.nodes_group = pygame.sprite.Group()
        self.player = None

        # Mixer
        self.mixer = Mixer()

        # Constroi o mapa
        self.make_map(self.map)
        self.mixer.play_hyrule()

    # Define as propriedades do mapa
    def make_map(self, map):
        self.map = map

        # Constroi o grid (matriz de nodes)
        self.map.set_nodes()

        # Define os vizinhos de cada node e os adiciona ao grupo de nodes
        for row in self.map.nodes:
            for node in row:
                self.nodes_group.add(node)
                node.update_neighbors(self.map.nodes)

        # Define o ponto inicial do mapa e a posicao do jogador
        if self.map.start_point:
            self.map.set_start_node()
            self.player = make_start(self.map.start_node.get_coord())

        # Define o ponto final do mapa, caso esse seja estabelecido
        if self.map.end_point:
            self.map.set_end_node()

        # Define a janela e o seu tamanho
        pygame.display.quit()
        pygame.display.init()

        title = f'Zelda Astar - {" ".join(self.map.name.capitalize().split("_"))}'
        pygame.display.set_caption(title)

        self.width = 504 if self.map.is_dungeon() else 756
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
            self.mixer.unpause_hyrule()
            self.toggle_state = False

        if self.state == 'dungeon_1' and self.toggle_state:
            self.make_map(dungeon_1())
            self.mixer.play_dungeon(1)
            self.toggle_state = False

        if self.state == 'dungeon_2' and self.toggle_state:
            self.make_map(dungeon_2())
            self.mixer.play_dungeon(2)
            self.toggle_state = False

        if self.state == 'dungeon_3' and self.toggle_state:
            self.make_map(dungeon_3())
            self.mixer.play_dungeon(3)
            self.toggle_state = False

    # Inicia o jogo
    def start(self):
        if self.state == 'hyrule':
            self.reconstruct_path(
                self.current_path,
                list(reversed(self.current_path))
            )

        else:
            best_way = algorithm(
                self.map,
                self.map.start_node,
                self.map.end_node
            )

            self.reconstruct_path(best_way, list(reversed(best_way)))

    # Atualiza os nodes que definem o caminho encontrado pelo algoritmo
    def reconstruct_path(self, path, reverse_path):

        # Em Hyrule -> anda até a entrada da dungeon e entra
        if self.state == 'hyrule':

            # Percorre ate o ponto final
            self.total_cost = move(self.window, self.state, self.player,
                                   self.total_cost, self.width, self.current_order, path)

            # Entra na dungeon, caso o player nao tenha chegado ao objetivo final
            if self.order[0] != 'entrada_lost_woods':
                (start, end) = self.current_order
                self.current_order = (f'entrada_{end}', 'pingente')
                print(
                    f'\rtotal_cost: {self.total_cost}, cost: 0, entrada_{end} --> pingente', end='')
                self.current_start_point = self.current_end_point
                self.toggle_state = True
                self.state = self.order.pop(0)

            # Chega a entrada de lost woods (caminhando lentamente e com estilo)
            else:
                (start, end) = self.current_order
                self.current_order = (end, 'master_sword')
                print(
                    f'\rtotal_cost: {self.total_cost}, cost: 0, {end} --> master_sword', end='')
                self.map.start_point = self.current_end_point
                self.map.end_point = self.points['master_sword']
                self.map.set_start_node()
                self.map.set_end_node()

                final_path = algorithm(
                    self.map, self.map.start_node, self.map.end_node)

                self.mixer.fadeout_hyrule()
                pygame.time.delay(500)  # Pausa dramática
                self.total_cost = move(self.window, self.state, self.player,
                                       self.total_cost, self.width, self.current_order, final_path, 200)
                self.mixer.play_winner()

                self.finished = True
                self.running = False

        # Nas Dungeons -> pega o pingente e volta para Hyrule
        else:
            # Vai até o pingente
            self.total_cost = move(self.window, self.state, self.player,
                                   self.total_cost, self.width, self.current_order, path)

            # Pega o pingente
            (start, end) = self.current_order
            self.current_order = (
                'pingente', f'saida_{start.split("entrada_")[1]}')
            print(
                f'\rtotal_cost: {self.total_cost}, cost: 0, pingente --> saida_{start.split("entrada_")[1]}', end='')

            self.mixer.play_get_pingente()
            pygame.time.delay(2000)

            # Volta para a entrada da dungeon
            self.total_cost = move(self.window, self.state, self.player, self.total_cost,
                                   self.width, self.current_order, reverse_path, 60, (255, 255, 255))

            # Sai da dungeon
            (start, end) = self.current_order
            self.current_order = (end.split('saida_')[1], self.order[0])
            print(
                f'\rtotal_cost: {self.total_cost}, cost: 0, {end.split("saida_")[1]} --> {self.order[0]}', end='')
            self.current_end_point = self.points[self.order[0]]
            self.toggle_state = True
            self.state = 'hyrule'

    # Desenha a grade
    def draw_grid(self):
        for i in range(self.map.size + 1):
            pygame.draw.line(
                self.window, GRAY,
                (0, i * NODE_SIZE),
                (self.width, i * NODE_SIZE)
            )
            for j in range(self.map.size):
                pygame.draw.line(
                    self.window, GRAY,
                    (j * NODE_SIZE, 0),
                    (j * NODE_SIZE, self.width)
                )

    # Desenha na tela
    def draw(self):
        # Desenha os nodes na tela
        self.nodes_group.draw(self.window)

        # Desenha a grade que separa os nodes
        if self.state == 'hyrule':
            self.draw_grid()

        # Desenha as imagens no mapa de Hyrule
        if not self.map.is_dungeon():
            for local, coord in self.points.items():
                node = self.map.get_node(coord)
                artifact_name = 'entrada_dungeon' if 'dungeon' in local else local
                node.set_artifact(artifact_name)
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

        rect = pygame.Surface((225, 30))
        rect.fill((50, 50, 50))
        self.window.blit(rect, (self.width - 225, 0))

        text_total_cost = '{:4}'.format(self.total_cost)
        title = render(
            f'CUSTO TOTAL: {text_total_cost},  CUSTO:    0', CPG11, RED, BLACK)
        title_rect = title.get_rect(center=(self.width - 110, 15))
        self.window.blit(title, title_rect)

        # Atualiza a tela
        pygame.display.update()
