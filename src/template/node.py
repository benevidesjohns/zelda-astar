import pygame


class Artifact(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(f'assets/img/artifacts/{image}.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Node(pygame.sprite.Sprite):
    def __init__(self, row, col, size, terrain, total_rows):
        super().__init__()
        self.size = size
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.total_rows = total_rows
        self.cost = terrain.cost
        self.image = pygame.image.load(f'assets/img/terrains/{terrain.image}.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.artifact = pygame.sprite.Group()
        self.artifact_name = ''
        self.neighbors = []


    # Retorna a posicao desse node na janela do pygame
    def get_coord(self):
        return self.x, self.y
    
    # Retorna a posicao desse node no grid
    def get_pos(self):
        return self.row, self.col
    
    # Define o artifact a ser desenhado sobre esse node
    def set_artifact(self, image):
        self.artifact.add(Artifact(image, self.x, self.y))
        self.artifact_name = image

    # Atualiza os vizinhos do node atual
    def update_neighbors(self, grid):
        self.neighbors = []

        # Verifica se pode existir um vizinho embaixo desse node
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].cost is None:
            self.neighbors.append(grid[self.row + 1][self.col])

        # Verifica se pode existir um vizinho em cima desse node
        if self.row > 0 and not grid[self.row - 1][self.col].cost is None:
            self.neighbors.append(grid[self.row - 1][self.col])

        # Verifica se pode existir um vizinho a direita desse node
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].cost is None:
            self.neighbors.append(grid[self.row][self.col + 1])

        # Verifica se pode existir um vizinho a esquerda desse node
        if self.col > 0 and not grid[self.row][self.col - 1].cost is None:
            self.neighbors.append(grid[self.row][self.col - 1])

