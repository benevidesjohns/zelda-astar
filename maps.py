from terrain import get_terrain

class Map:

    def __init__(self, size, start_point, end_point, terrains):
        self.size = size
        self.start_point = start_point
        self.end_point = end_point
        self.terrains = terrains


# map_hyrule = Map(
#     size = 48,
#     start = (37, 20),
#     end = (7,6),
# )

def hyrule():
    pass


def dungeon1():

    codes = [
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        'OLLLOOOOOOOOOOOOOOOOOLLLOOOO',
        'OLLLOOOOOOOOLLLOOOOOOLLLOOOO',
        'OOLOOOOLLLLLLLLOOOOOOLLLOOOO',
        'OOLOOOOLOOOOLLLOOOOOOOLOOOOO',
        'OOLLLLLLOOOOOOOOOOOOOOLOOOOO',
        'OOLOOOOOOOOOOOOOOOOOOOLOOOOO',
        'OOLOOOOOOOOOOOOOOOOLLLLLLLOO',
        'OOLOOOOOOOOLLLLLOOOLLLLLLLOO',
        'OOLLLLLLOOOLLLLLOOOLLLLLLLOO',
        'OOOLOOOLOOOLLLLLOOOLLLLLLLOO',
        'OOOLOOOLOOOOOLOOOOOOOOLOOOOO',
        'OOLLLOOLOOOOOLOOOOOOOOLOOOOO',
        'OOLLLOOLOOOOOLOOOOOOLLLLLOOO',
        'OOLLLOOLOOOOOLOOOOOOLOOOLOOO',
        'OOOOOOOLLLLLLLLLLLLLLOOOLOOO',
        'OOOOOOOLOOOOOOOOOOOOLOOOLOOO',
        'OOOOOOOLOOOOOOOOOOOOLOOOLOOO',
        'OOLLLOOLOOLLLOOOOOLLLLOOLOOO',
        'OOLLLLLLLLLLLOOOOOLLLLOOLOOO',
        'OOLLLOOLOOLLLOOOOOLLLLOOLOOO',
        'OOOOOOOLOOOOOOOOOOOOOOOOLOOO',
        'OOOOOOOLOOOOOOLLLLLLLLLLLOOO',
        'OOOOOOLLLLOOOOLOOOOOOOOOOOOO',
        'OOOOOOLLLLOOOOLOOOOOOOOOOOOO',
        'OOOOOOLLLLOOLLLLLOOOOOOOOOOO',
        'OOOOOOOOOOOOLLLLLOOOOOOOOOOO',
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOO',
    ]

    terrains = []
    for i, row in enumerate(codes):
        terrains.append([])
        for code in row:
            terrains[i].append(get_terrain(code))

    return Map(
        size = 28,
        start_point = (26, 14),
        end_point = (3, 13),
        terrains = terrains
    )

def dungeon_2():
    pass

def dungeon3():
    codes = [
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        'OOOLLLLLLLLLLLLLLLLLLLLLLOOO',
        'OOOLOOOOOOOOOOOLOOOOOOOOLOOO',
        'OOOLOOOOOOOOOOOLOOOOOOOOLOOO',
        'OOOLOOLLLOLLLOLLLOLLLOOOLOOO',
        'OOOLOOLLLLLLLOLLLOLLLOOOLOOO',
        'OOOLOOLLLOLLLOLLLOLLLOOOLOOO',
        'OOOLOOOOOOOLOOOLOOOLOOOOLOOO',
        'OOOLOOLLLOOLOOOLOOOLOLLOLOOO',
        'OOOLLLLLLLLLLLLLLLLLLLLOLOOO',
        'OOOLOOLLLOOLOOOOOOOLOLLOLOOO',
        'OOOLOOOLOOOLOOOOOOOLOOOOLOOO',
        'OOOLOOLLLOLLLOLLLOLLLOOOLOOO',
        'OOOLOOLLLOLLLLLLLOLLLOOOLOOO',
        'OOOLOOLLLOLLLOLLLOLLLOOOLOOO',
        'OOOLOOOLOOOOOOOLOOOOOOOOLOOO',
        'OOOLOOLLLOOOOLLLLLOOLLLOLOOO',
        'OOOLOOLLLOOOOLLLLLOOLLLOLOOO',
        'OOOLOOOOOOOOOOOOOOOOOLOOLOOO',
        'OOOLLLLLLLLLLLLLLLLLLLLLLOOO',
        'OOOOOOLOOOOOOOLOOOOOOLOOOOOO',
        'OOOOOOLOOOOOOOLOOOOOOLOOOOOO',
        'OOOOLLLLLOOOLLLLLOOLLLLLOOOO',
        'OOOOLLLLLOOOLLLLLOOLLLLLOOOO',
        'OOOOLLLLLOOOLLLLLOOLLLLLOOOO',
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOO',
    ]

    terrains = []
    for i, row in enumerate(codes):
        terrains.append([])
        for code in row:
            terrains[i].append(get_terrain(code))

    return Map(
        size = 28,
        start_point = (25, 14),
        end_point = (19, 15),
        terrains = terrains
    )
