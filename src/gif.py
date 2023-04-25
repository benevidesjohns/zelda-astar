import pygame
import sys
from PIL import Image

from .utils.outlined_font import render
from .utils.constants import FORMAT, FONT_GAME_END, BORDER_TEXT_COLOR, TEXT_COLOR


def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)


def get_gif_frame(img, frame):
    img.seek(frame)
    return img.convert(FORMAT)


def get_formatted_text(text, dots, statistic, type):
    if(type == 'list'):
        formatted_statistic = ' --> '.join([statistic[i] for i in range(len(statistic))])
    elif(type == 'float'):
        formatted_statistic = '{:.3f}s'.format(statistic)
    elif(type == 'int'):
        formatted_statistic = f'{statistic}'

    return f'{text} {". " * dots} {formatted_statistic}'


def run(gif_image, statistics):
    (total_cost, total_cost_type) = statistics['total_cost']
    (elapsed_time, elapsed_time_type) = statistics['elapsed_time']
    (best_order, best_order_type) = statistics['best_order']

    texts = []
    texts.append(get_formatted_text('CUSTO  TOTAL', 30, total_cost, total_cost_type))
    texts.append(get_formatted_text('TEMPO  DECORRIDO ', 21, elapsed_time, elapsed_time_type))
    texts.append(get_formatted_text('MELHOR  CAMINHO', 11, best_order, best_order_type))
    
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
        rect.set_alpha(80)
        rect.fill((255, 255, 255))
        screen.blit(rect, (0, 0))

        # Desenha as estatísticas na tela
        title = render('PARABÉNS!  VOCÊ  VENCEU!', FONT_GAME_END, TEXT_COLOR, BORDER_TEXT_COLOR)
        title_rect = title.get_rect(center=(gif_img.width // 2, 20))
        screen.blit(title, title_rect)

        for i, text in enumerate(texts):
            screen.blit(render(text, FONT_GAME_END, TEXT_COLOR, BORDER_TEXT_COLOR), (20, 142 + 35*i))

        game = render('ZELDA  ASTAR', FONT_GAME_END, TEXT_COLOR, BORDER_TEXT_COLOR)
        game_rect = game.get_rect(center=(gif_img.width // 2, gif_img.height - 50))
        screen.blit(game, game_rect)

        credits = render('FEITO COM  <3  BY:  WILLIAM  E  JOÃO', FONT_GAME_END, TEXT_COLOR, BORDER_TEXT_COLOR)
        credits_rect = credits.get_rect(center=(gif_img.width // 2, gif_img.height - 20))
        screen.blit(credits, credits_rect)
        
        pygame.display.update()
        clock.tick(10)
