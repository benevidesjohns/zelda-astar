import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('assets/img/link_18x18.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position

# Cria o jogador no ponto onde ele vai comecar
def make_start(point):
    player = Player(point)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    return player_group