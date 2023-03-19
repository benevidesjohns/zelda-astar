from terrain import get_terrain
import os

class Map:

    def __init__(self, size, start_point, end_point, terrains):
        self.size = size
        self.start_point = start_point
        self.end_point = end_point
        self.terrains = terrains
        self.nodes = []


    def set_start_point(self, point):
        x, y = point
        self.start_point = (x, y)


    def set_end_point(self, point):
        x, y = point
        self.end_point = (x, y)


    def set_nodes(self, nodes):
        self.nodes = nodes


def get_map_code(map_name):
    map_code = {
        'HYRULE': [],
        'DUNGEON1': [],
        'DUNGEON2': [],
        'DUNGEON3': [],
    }

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

    return map_code[map_name]


def get_map_terrains(codes):
    terrains = []
    for i, row in enumerate(codes):
        terrains.append([])
        for code in row:
            terrains[i].append(get_terrain(code))
    
    return terrains


def hyrule():
    codes = get_map_code('HYRULE')
    terrains = get_map_terrains(codes)

    return Map(
        size=42,
        start_point=(37, 20),
        end_point=(7, 6),
        terrains=terrains
    )


def dungeon1():
    codes = get_map_code('DUNGEON1')
    terrains = get_map_terrains(codes)

    return Map(
        size=28,
        start_point=(26, 14),
        end_point=(3, 13),
        terrains=terrains
    )


def dungeon2():
    codes = get_map_code('DUNGEON2')
    terrains = get_map_terrains(codes)

    return Map(
        size=28,
        start_point=(25, 13),
        end_point=(2, 13),
        terrains=terrains
    )


def dungeon3():
    codes = get_map_code('DUNGEON3')
    terrains = get_map_terrains(codes)

    return Map(
        size=28,
        start_point=(25, 14),
        end_point=(19, 15),
        terrains=terrains
    )
