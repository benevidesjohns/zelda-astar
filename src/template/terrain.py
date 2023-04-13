TERRAINS = {
    'G': ['gram', 10],
    'S': ['sand', 20],
    'F': ['forest', 100],
    'M': ['montain', 150],
    'W': ['water', 180],
    'L': ['floor', 10],
    'O': ['wall', None],
}


class Terrain:

    def __init__(self, cost, image):
        self.cost = cost
        self.image = image


# Retorna um terreno
def get_terrain(code):
    [image, cost] = TERRAINS[code]
    return Terrain(cost=cost, image=image)
