import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    def __init__(self, image, image_boom, w, h,  *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = image
        self.image_boom = image_boom
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(w)
        self.rect.y = random.randrange(h)

    def explode(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.image = self.image_boom

    def update(self, *args):
        if args:
            self.explode(args[0])


def game(screen):
    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()
    bombs_group = pygame.sprite.Group()
    bomb_img = load_image("bomb.png")
    boom_img = load_image("boom.png")
    for _ in range(50):
        Bomb(bomb_img, boom_img, width, height, bombs_group, all_sprites)

    FPS = 60
    tick = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        tick += 1
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    game(screen)