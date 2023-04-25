import pygame
import sys
from PIL import Image

from .outlined_font import render

FORMAT = "RGBA"
BLACK_COLOR = (70, 70, 70)
GREEN_COLOR = (120, 235, 20)
pygame.font.init()
FONT = pygame.font.SysFont('arial', 30, True, False)

def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)


def get_gif_frame(img, frame):
    img.seek(frame)
    return img.convert(FORMAT)


def get_formatted_text(text, statistic, type):
    if(type == 'list'):
        formatted_statistic = ' --> '.join([statistic[i] for i in range(len(statistic))])
    elif(type == 'float'):
        formatted_statistic = '{:.3f}s'.format(statistic)
    elif(type == 'int'):
        formatted_statistic = f'{statistic}'

    return f'{text}: {formatted_statistic}' if text else formatted_statistic
    # text_render = f'{text}: {formatted_statistic}' if text else formatted_statistic
    # return FONT.render(text_render, True, BLACK_COLOR)


def run(gif_image, statistics):
    (total_cost, total_cost_type) = statistics['total_cost']
    (elapsed_time, elapsed_time_type) = statistics['elapsed_time']
    (best_order, best_order_type) = statistics['best_order']

    texts = []
    texts.append(get_formatted_text('Custo total', total_cost, total_cost_type))
    texts.append(get_formatted_text('Tempo decorrido', elapsed_time, elapsed_time_type))
    texts.append('Ordem das dungeons:')
    texts.append(get_formatted_text('', best_order, best_order_type))
    
    # Carrega a imagem do gif
    gif_img = Image.open(gif_image)
    if not getattr(gif_img, "is_animated", False):
        print(f"Imagem em {gif_image} não é um gif animado")
        return

    # Carrega a janela do pygame
    screen = pygame.display.set_mode((gif_img.width, gif_img.height))
    pygame.display.set_caption('Zelda Astar - YOU WIN')

    current_frame = 0
    clock = pygame.time.Clock()

    while True:
        frame = pil_to_game(get_gif_frame(gif_img, current_frame))
        screen.blit(frame, (0, 0))

        # Gerencia os eventos do pygame
        for event in pygame.event.get():

            # Verifica as teclas do teclado
            if event.type == pygame.KEYDOWN:

                # ESC - Encerra o jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Atualiza a tela do pygame
        current_frame = (current_frame + 1) % gif_img.n_frames

        rect = pygame.Surface((gif_img.width, gif_img.height)) 
        rect.set_alpha(128)
        rect.fill((255, 255, 255))
        screen.blit(rect, (0, 0))

        # Desenha as estatísticas na tela
        title = render('Parabéns! Você venceu!', FONT, GREEN_COLOR, BLACK_COLOR)
        title_rect = title.get_rect(center=(gif_img.width // 2, 20))
        screen.blit(title, title_rect)

        for i, text in enumerate(texts):
            screen.blit(render(text, FONT, GREEN_COLOR, BLACK_COLOR), (20, 142 + 30*i))

        credits = render('Feito com <3 by: William e João', FONT, GREEN_COLOR, BLACK_COLOR)
        credits_rect = credits.get_rect(center=(gif_img.width // 2, gif_img.height - 40))
        screen.blit(credits, credits_rect)
        
        pygame.display.update()
        clock.tick(10)
