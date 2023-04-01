CODE = {
    'GRAM': 'G',
    'SAND': 'S',
    'FOREST': 'F',
    'MONTAIN': 'M',
    'WATER': 'W',
    'DUNGEON_FLOOR': 'L',
    'DUNGEON_WALL': 'O'
}


class Terrain:

    def __init__(self, code, cost, image):
        self.code = code
        self.cost = cost
        self.image = image

# Retorna um terreno


def get_terrain(code):

    # Grama
    if code == CODE['GRAM']:
        return Terrain(
            code,
            cost=10,
            image='gram'
        )

    # Areia
    elif code == CODE['SAND']:
        return Terrain(
            code,
            cost=20,
            image='sand'
        )

    # Floresta
    elif code == CODE['FOREST']:
        return Terrain(
            code,
            cost=100,
            image='forest'
        )

    # Montanha
    elif code == CODE['MONTAIN']:
        return Terrain(
            code,
            cost=150,
            image='montain'
        )

    # Agua
    elif code == CODE['WATER']:
        return Terrain(
            code,
            cost=180,
            image='water'
        )

    # Piso da Dungeon
    elif code == CODE['DUNGEON_FLOOR']:
        return Terrain(
            code,
            cost=10,
            image='floor'
        )

    # Parede da Dungeon
    elif code == CODE['DUNGEON_WALL']:
        return Terrain(
            code,
            cost=None,
            image='wall'
        )
