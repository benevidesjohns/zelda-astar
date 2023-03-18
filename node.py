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
    

    # Desenha o node no grid
    def draw(self, window):
        pygame.draw.rect(
            window,
            self.terrain.color,
            pygame.Rect(self.x, self.y, self.size, self.size)
        )


    # Altera a cor do terreno para representar o caminho que o algoritmo encontrou
    def make_path(self):
        self.terrain = Terrain(
            code = self.terrain.code,
            cost = self.terrain.cost,
            color = (128, 0, 128)
        )

    # Altera a cor do terreno para representar o caminho que o algoritmo encontrou
    def make_start(self):
        self.terrain = Terrain(
            code = self.terrain.code,
            cost = self.terrain.cost,
            color = (255, 165, 0)
        )

    # Altera a cor do terreno para representar o caminho que o algoritmo encontrou
    def make_end(self):
        self.terrain = Terrain(
            code = self.terrain.code,
            cost = self.terrain.cost,
            color = (64, 224, 208)
        )


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

