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

    def __init__(self, code, cost, color):
        self.code = code
        self.cost = cost
        self.color = color

def get_terrain(code):

    # Grama
    if code == CODE['GRAM']:
        return Terrain(
            code,
            cost = 10,
            color = (51, 204, 51)
        )
    
    # Areia
    elif code == CODE['SAND']:
        return Terrain(
            code,
            cost = 20,
            color = (196, 189, 146)
        )
    
    # Floresta
    elif code == CODE['FOREST']:
        return Terrain(
            code,
            cost = 100,
            color = (0, 153, 0)
        )
    
    # Montanha
    elif code == CODE['MONTAIN']:
        return Terrain(
            code,
            cost = 150,
            color = (144, 138, 77)
        )
    
    # Agua
    elif code == CODE['WATER']:
        return Terrain(
            code,
            cost = 180,
            # color = (88, 140, 205)
            color = (51, 204, 255)
        )
    
    # Piso da Dungeon
    elif code == CODE['DUNGEON_FLOOR']:
        return Terrain(
            code,
            cost = 10,
            color = (226, 226, 226)
        )
    
    # Parede da Dungeon
    elif code == CODE['DUNGEON_WALL']:
        return Terrain(
            code,
            cost = None,
            color = (184, 184, 184)
        )
