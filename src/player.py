import pygame
import sys

from .utils.constants import CPG11, GRAY, RED, BLACK, NODE_SIZE
from .utils.outlined_font import render


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('assets/img/link.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position


# Faz a animacao do player andando no mapa
def move(window, state, player_group, total_cost, width, current_order, path, delay=60, trace_color=BLACK):
    current_cost = 0
    for i, node in enumerate(path):

        # Gerencia os eventos do pygame
        for event in pygame.event.get():

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # ESC - Encerra o jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Calcula o custo
        if node != path[0]:
            current_cost += node.cost
            total_cost += node.cost
        (start, end) = current_order
        print(
            f'\rtotal_cost: {total_cost}, cost: {current_cost}, {start} --> {end}', end='')

        # Desenha o player
        player = Player(node.get_coord())
        player_group.add(player)
        player_group.draw(window)
        pygame.display.update()
        pygame.time.delay(delay)

        # Remove o player caso não tenha chegado no final do path
        if node != path[-1]:
            player_group.add(node)
            player_group.draw(window)
            player_group.empty()

        # Redesenha a grade em torno do node atual
        if state == 'hyrule':
            x, y = node.get_coord()
            pygame.draw.line(
                window, GRAY, (x, y), (x+NODE_SIZE, y)
            )
            pygame.draw.line(
                window, GRAY, (x, y+NODE_SIZE), (x+NODE_SIZE, y+NODE_SIZE)
            )
            pygame.draw.line(
                window, GRAY, (x, y), (x, y+NODE_SIZE)
            )
            pygame.draw.line(
                window, GRAY, (x+NODE_SIZE, y), (x+NODE_SIZE, y+NODE_SIZE)
            )

        # Desenha o rastro do personagem
        if node != path[-1]:
            next_node = path[i+1]
            xi, yi = node.get_coord()
            xf, yf = next_node.get_coord()

            pygame.draw.line(
                window, trace_color,
                (xi+(NODE_SIZE//2), yi+(NODE_SIZE//2)),
                (xf+(NODE_SIZE//2), yf+(NODE_SIZE//2)), 4
            )

        # Redesenha os artifacts
        if not node.artifact is None and 'pingente' not in node.artifact_name:
            node.artifact.draw(window)

        # Atualiza os custos a serem exibidos na tela
        rect = pygame.Surface((225, 30))
        rect.fill((50, 50, 50))
        window.blit(rect, (width - 225, 0))

        text_total_cost = '{:4}'.format(total_cost)
        title = render(
            f'CUSTO TOTAL: {text_total_cost},  CUSTO: {current_cost}', CPG11, RED, GRAY)
        title_rect = title.get_rect(center=(width - 110, 15))
        window.blit(title, title_rect)

        pygame.display.update()

    print('\n')

    return total_cost


# Cria o jogador no ponto onde ele vai comecar
def make_start(point):
    player = Player(point)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    return player_group
