from terrain import Terrain
import pygame

class Node:
    def __init__(self, row, col, size, terrain, total_rows):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.total_rows = total_rows
        self.terrain = terrain
        self.neighbors = []
        self.size = size


    # Retorna a posicao desse node no grid
    def get_pos(self):
        return self.row, self.col
    

    # Desenha a imagem do node
    def draw(self, window):
        img = pygame.image.load(f'img/terrains/{self.terrain.image}.png')
        window.blit(img, (self.x, self.y))

    
    # Desenha uma imagem na mesma posicao do node
    def draw_image(self, window, image):
        img = pygame.image.load(f'img/{image}_18x18.png')
        window.blit(img, (self.x, self.y))
        

    # Terrenos impossiveis de atravessar (paredes das Dungeons)
    def is_blocked(self):
        return self.terrain.cost is None
    
    
    # Atualiza os vizinhos do node atual
    def update_neighbors(self, grid):
        self.neighbors = []

        # Verifica se pode existir um vizinho embaixo desse node
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_blocked():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Verifica se pode existir um vizinho em cima desse node
        if self.row > 0 and not grid[self.row - 1][self.col].is_blocked():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Verifica se pode existir um vizinho a direita desse node
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_blocked():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Verifica se pode existir um vizinho a esquerda desse node
        if self.col > 0 and not grid[self.row][self.col - 1].is_blocked():
            self.neighbors.append(grid[self.row][self.col - 1])

