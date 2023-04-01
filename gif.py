import pygame
import sys
from PIL import Image

size=(756,422)
FORMAT = "RGBA"


def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)

def get_gif_frame(img, frame):
    img.seek(frame)
    return  img.convert(FORMAT)


def init():
    return pygame.display.set_mode((756, 422))

def exit():
    pygame.quit()


def main(screen, path_to_image):
    gif_img = Image.open(path_to_image)
    if not getattr(gif_img, "is_animated", False):
        print(f"Imagem em {path_to_image} não é um gif animado")
        return
    current_frame = 0
    clock = pygame.time.Clock()
    while True:
        frame = pil_to_game(get_gif_frame(gif_img, current_frame))
        screen.blit(frame, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                # ESC - Encerra o jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        current_frame = (current_frame + 1) % gif_img.n_frames

        pygame.display.flip()
        clock.tick(10)