
terrenos = {
    'agua': {'cor': 'BLUE', 'cost': ''}
}

class Node:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.cost = terrain['cost']
        self.color = terrain['color']


    # Terrenos impossiveis de atravessar (paredes das Dungeons)
    def is_blocked(self):
        return self.cost is None

