from terrain import get_terrain
import os


class Map:

    def __init__(self, name, size, start_point, end_point, terrains):
        self.name = name
        self.size = size
        self.start_point = start_point
        self.end_point = end_point
        self.terrains = terrains
        self.nodes = []
        self.start_node = None
        self.end_node = None

    # Verifica se o mapa é uma dungeon
    def is_dungeon(self):
        return self.size == 28

    # Seta um ponto inicial no mapa
    def set_start_point(self, point):
        x, y = point
        self.start_point = (x, y)

    # Seta um ponto final no mapa
    def set_end_point(self, point):
        x, y = point
        self.end_point = (x, y)

    # Seta uma lista de nodes no mapa
    def set_nodes(self, nodes):
        self.nodes = nodes

    # Seta os nodes inicial e final do mapa
    def set_start_node(self):
        (x, y) = self.start_point
        self.start_node = self.nodes[x][y]

    def set_end_node(self):
        (x, y) = self.end_point
        self.end_node = self.nodes[x][y]
    
    # Retorna um node a partir de um ponto
    def get_node(self, point):
        x, y = point
        return self.nodes[x][y]

# Retorna os códigos de um mapa
def get_map_code(map_name):
    map_code = {
        'HYRULE': [],
        'DUNGEON1': [],
        'DUNGEON2': [],
        'DUNGEON3': [],
    }

    # Lê o arquivo com os códigos dos mapas
    with open(f'{os.getcwd()}/maps_codes.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('\n')[0]

            # Ignora linhas em branco
            if len(line.strip()) == 0:
                continue

            # Verifica qual o mapa atual
            if line in map_code.keys():
                current_map = line

            # Salva as linhas do mapa
            else:
                map_code[current_map].append(line)

    # Retorna um dicionário com o nome e os códigos do mapa
    return map_code[map_name]

# Retorna os terrenos do mapa
def get_map_terrains(codes):
    terrains = []
    for i, row in enumerate(codes):
        terrains.append([])
        for code in row:
            terrains[i].append(get_terrain(code))

    return terrains

# Retorna o mapa de hyrule
def hyrule(start, end):
    codes = get_map_code('HYRULE')
    terrains = get_map_terrains(codes)

    return Map(
        name='hyrule',
        size=42,
        start_point=start,
        end_point=end,
        terrains=terrains
    )

# Retorna o mapa da dungeon 1
def dungeon_1():
    codes = get_map_code('DUNGEON1')
    terrains = get_map_terrains(codes)

    return Map(
        name='dungeon_1',
        size=28,
        start_point=(26, 14),
        end_point=(3, 13),
        terrains=terrains
    )

# Retorna o mapa da dungeon 2
def dungeon_2():
    codes = get_map_code('DUNGEON2')
    terrains = get_map_terrains(codes)

    return Map(
        name='dungeon_2',
        size=28,
        start_point=(25, 13),
        end_point=(2, 13),
        terrains=terrains
    )

# Retorna o mapa da dungeon 3
def dungeon_3():
    codes = get_map_code('DUNGEON3')
    terrains = get_map_terrains(codes)

    return Map(
        name='dungeon_3',
        size=28,
        start_point=(25, 14),
        end_point=(19, 15),
        terrains=terrains
    )
