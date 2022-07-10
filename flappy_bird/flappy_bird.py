import pygame
import random


class GameScreen():
    def __init__(self, height=500, width=500, caption='Flappy Bird'):
        self.screen_height = height
        self.screen_width = width
        self.caption = caption

    def create_screen(self):
        screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption(self.caption)

        return screen


class BgFence(GameScreen):

    def __init__(self, game_screen, bg_img='images/bg.png', fence_img='images/fence.png'):
        self.gs = game_screen
        self.bg_img = bg_img
        self.fence_img = fence_img

        self.bg = pygame.image.load(self.bg_img)
        self.fence = pygame.image.load(self.fence_img)

        self.fence_y = self.gs.screen_height - 40
        self.fences = [{'x': 0, 'y': self.fence_y}]

    def update_bg_fence(self, screen):
        screen.blit(self.bg, (0, 0))

        for fence in self.fences:
            fence['x'] -= 10
            screen.blit(self.fence, (fence['x'], fence['y']))

        fence_w = self.fence.get_width()

        # add fence
        if self.fences[-1]['x'] <= (self.gs.screen_width + fence_w):
            fence_x = self.fences[-1]['x'] + fence_w
            self.fences.append({'x': fence_x, 'y': self.fence_y})

        # remove fence
        if self.fences[0]['x'] + fence_w < 0:
            self.fences.pop(0)


class Bird():
    pass


class Pipe():
    pass
