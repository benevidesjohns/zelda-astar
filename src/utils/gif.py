import pygame
import sys
from PIL import Image

FORMAT = "RGBA"


def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)


def get_gif_frame(img, frame):
    img.seek(frame)
    return img.convert(FORMAT)


def run(gif_image):

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
        pygame.display.update()
        clock.tick(10)
