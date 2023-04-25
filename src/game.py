from .template.maps import hyrule, dungeon_1, dungeon_2, dungeon_3
from .player import Player, make_start
from .utils.algorithm import algorithm
from itertools import permutations
from pygame import mixer
import pygame


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

        # Pygame Mixer
        self.hyrule_song = self.create_song('lost_woods')
        self.dungeon_song1 = self.create_song('song_of_storms', 0.7)
        self.dungeon_song2 = self.create_song('meet_zelda_again', 0.7)
        self.dungeon_song3 = self.create_song('mayors_meeting', 0.7)
        self.get_pingente = self.create_song('small_item_get', 0.5)
        # self.winner_song = self.create_song('ikana_castle')
        self.winner_song = self.create_song('hyrule')

        self.ch_hyrule = mixer.Channel(0)
        self.ch_dungeon = [mixer.Channel(i) for i in range(1, 4)]
        self.ch_winner = mixer.Channel(4)
        self.ch_pingente = mixer.Channel(5)

        # Constroi o mapa
        self.make_map(self.map)
        self.ch_hyrule.play(self.hyrule_song)

    # Criador de sons
    def create_song(self, path, volume=1):
        mixer.init()
        sound = mixer.Sound(f'assets/audio/{path}.mp3')
        sound.set_volume(volume)
        return sound

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

            for ch_dungeon in self.ch_dungeon:
                ch_dungeon.stop()
            self.ch_hyrule.unpause()

            self.toggle_state = False

        if self.state == 'dungeon_1' and self.toggle_state:
            self.make_map(dungeon_1())

            self.ch_hyrule.pause()
            self.ch_dungeon[0].play(self.dungeon_song1)

            self.toggle_state = False

        if self.state == 'dungeon_2' and self.toggle_state:
            self.make_map(dungeon_2())

            self.ch_hyrule.pause()
            self.ch_dungeon[1].play(self.dungeon_song2)

            self.toggle_state = False

        if self.state == 'dungeon_3' and self.toggle_state:
            self.make_map(dungeon_3())

            self.ch_hyrule.pause()
            self.ch_dungeon[2].play(self.dungeon_song3)

            self.toggle_state = False

    # Define a melhor ordem para passar pelas dungeons
    def set_best_order(self):

        # Pontos de referência
        start = self.current_start_point
        dungeons = [self.points[f'dungeon_{i}'] for i in range(1, 4)]
        end = self.points['entrada_lost_woods']

        # Obtem o melhor caminho entre os pontos de referência
        paths = {}
        for i in range(len(dungeons)):
            paths[f'start-dungeon_{i+1}'] = algorithm(
                self.map, self.map.get_node(start),
                self.map.get_node(dungeons[i])
            )
            paths[f'dungeon_{i+1}-entrada_lost_woods'] = algorithm(
                self.map, self.map.get_node(dungeons[i]),
                self.map.get_node(end)
            )
            for j in range(i+1, len(dungeons)):
                paths[f'dungeon_{i+1}-dungeon_{j+1}'] = algorithm(
                    self.map, self.map.get_node(dungeons[i]),
                    self.map.get_node(dungeons[j])
                )
                paths[f'dungeon_{j+1}-dungeon_{i+1}'] = list(
                    reversed(paths[f'dungeon_{i+1}-dungeon_{j+1}'])
                )

        print('\n----------------------------------------------- CUSTOS ----------------------------------------------\n')

        # Calcula os custos para cada caminho
        for key, nodes in paths.items():
            path_cost = sum(list(map(lambda node: node.cost, nodes)))
            self.costs[key] = path_cost - nodes[-1].cost
            (start, end) = key.split("-")
            start = '{:9}'.format(start)
            print(f'cost: {self.costs[key]}, path: {start} --> {end}')

        # Lista todas as ordens de caminhos possíveis
        permuts = list(permutations(['dungeon_1', 'dungeon_2', 'dungeon_3']))
        orders = list(map(
            lambda order: ['start'] + list(order) + ['entrada_lost_woods'],
            permuts
        ))

        # Soma os custos para todas as ordens de caminhos possíveis
        # e verifica a melhor ordem de caminho entre as dungeons
        order_paths = []
        best_cost = float("inf")
        best_order_path_index = 0

        for index, order in enumerate(orders):
            total_cost = 0

            for i in range(len(order)-1):
                total_cost += self.costs[f'{order[i]}-{order[i+1]}']

            order_paths.append({
                'total_cost': total_cost,
                'order': order
            })

            if total_cost < best_cost:
                best_cost = total_cost
                best_order_path_index = index

        print('\n---------------------------------- MELHOR CAMINHO ENTRE AS DUNGEONS ---------------------------------\n')
        print(order_paths[best_order_path_index])

        self.best_order = orders[best_order_path_index].copy()

        # Seleciona os paths da melhor ordem de caminho entre as dungeons
        best_order_path = order_paths[best_order_path_index]['order']
        best_paths = []
        for i in range(len(best_order_path)-1):
            best_paths.append(
                paths[f'{best_order_path[i]}-{best_order_path[i+1]}'])

        # Define o order path e o primeiro end point do mapa
        self.path = best_paths
        self.current_path = self.path.pop(0)

        self.order = order_paths[best_order_path_index]['order']
        self.current_order = (self.order.pop(0), self.order[0])

        self.map.end_point = self.current_end_point = self.points[self.order[0]]
        self.map.set_end_node()

        print('\n------------------------------------------ OUTROS CAMINHOS ------------------------------------------\n')
        for i in range(len(order_paths)):
            if i != best_order_path_index:
                print(order_paths[i], end='\n\n')

        print('\n----------------------------------------- CAMINHO PERCORRIDO -----------------------------------------\n')
        (start, end) = self.current_order
        print(
            f'\rtotal_cost: {self.total_cost}, cost: {self.total_cost}, {start} --> {end}', end='')

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

    # Faz a animacao do player andando no mapa
    def draw_player(self, path, delay, trace_color=(0,0,0)):
        current_cost = 0
        for i, node in enumerate(path):

            # Calcula o custo
            current_cost += node.cost
            self.total_cost += node.cost
            (start, end) = self.current_order
            print(
                f'\rtotal_cost: {self.total_cost}, cost: {current_cost}, {start} --> {end}', end='')

            # Desenha o player
            player = Player(node.get_coord())
            self.player.add(player)
            self.player.draw(self.window)
            pygame.display.update()
            pygame.time.delay(delay)

            # Remove o player caso não tenha chegado no final do path
            if node != path[-1]:
                self.player.add(node)
                self.player.draw(self.window)
                self.player.empty()

            # Redesenha a grade em torno do node atual
            if self.state == 'hyrule':
                x, y = node.get_coord()
                pygame.draw.line(
                    self.window, (70, 70, 70), (x, y), (x+18, y)
                )
                pygame.draw.line(
                    self.window, (70, 70, 70), (x, y+18), (x+18, y+18)
                )
                pygame.draw.line(
                    self.window, (70, 70, 70), (x, y), (x, y+18)
                )
                pygame.draw.line(
                    self.window, (70, 70, 70), (x+18, y), (x+18, y+18)
                )

            # Desenha o rastro do personagem
            if node != path[-1]:
                next_node = path[i+1]
                xi, yi = node.get_coord()
                xf, yf = next_node.get_coord()

                pygame.draw.line(
                    self.window, trace_color, (xi+9, yi+9), (xf+9, yf+9), 4
                )

            # Redesenha os artifacts
            if not node.artifact is None and 'pingente' not in node.artifact_name:
                node.artifact.draw(self.window)

            pygame.display.update()

        print('\n')

    # Atualiza os nodes que definem o caminho encontrado pelo algoritmo
    def reconstruct_path(self, path, reverse_path):

        # Em Hyrule -> anda até a entrada da dungeon e entra
        if self.state == 'hyrule':

            # Percorre ate o ponto final
            self.draw_player(path=path, delay=60)
            # self.draw_player(path=path, delay=1)

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

                # self.ch_hyrule.fadeout(3300)
                self.ch_hyrule.fadeout(500)
                self.ch_hyrule.stop()
                self.ch_winner.play(self.winner_song)
                pygame.time.delay(2000)  # Pausa dramática
                # pygame.time.delay(500)  # Pausa dramática
                self.draw_player(path=final_path, delay=450)

                # self.ch_hyrule.stop()
                # self.ch_winner.play(self.winner_song)
                self.finished = True
                self.running = False

        # Nas Dungeons -> pega o pingente e volta para Hyrule
        else:
            # Vai até o pingente
            self.draw_player(path=path, delay=50)

            # Pega o pingente
            (start, end) = self.current_order
            self.current_order = (
                'pingente', f'saida_{start.split("entrada_")[1]}')
            print(
                f'\rtotal_cost: {self.total_cost}, cost: 0, pingente --> saida_{start.split("entrada_")[1]}', end='')
            for ch in self.ch_dungeon:
                ch.set_volume(0.2)

            self.ch_pingente.play(self.get_pingente, maxtime=2000)
            pygame.time.delay(2000)

            for ch in self.ch_dungeon:
                ch.set_volume(0.7)

            # Volta para a entrada da dungeon
            self.draw_player(path=reverse_path, delay=50, trace_color=(255,255,255))

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
                self.window, (70, 70, 70), (0, i * 18),
                (self.width, i * 18)
            )
            for j in range(self.map.size):
                pygame.draw.line(
                    self.window, (70, 70, 70), (j * 18, 0),
                    (j * 18, self.width)
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

        # Atualiza a tela
        pygame.display.update()
        pygame.time.delay(delay)
