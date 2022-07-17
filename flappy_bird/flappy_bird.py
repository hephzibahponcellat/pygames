import pygame
import random


class GameScreen():
    def __init__(self):
        self.SCREEN_HEIGHT = 500
        self.SCREEN_WIDTH = 500
        self.CAPTION = 'Flappy Bird'

    def create_screen(self):
        screen = pygame.display.set_mode((self.SCREEN_HEIGHT, self.SCREEN_WIDTH))
        pygame.display.set_caption(self.CAPTION)

        return screen


class Score():
    def __init__(self):
        self.game_score = 0
        self.IMPACT_FONT = 'impact'
        self.IMPACT_FONT_SIZE = 40
        self.SCORE_POS = (250, 100)
        self.SCORE_COLOR = (255, 255, 0)

        pygame.font.init()
        self.score = pygame.font.SysFont(self.IMPACT_FONT, self.IMPACT_FONT_SIZE)

    def display_score(self, screen):
        score = str(self.game_score)
        label = self.score.render(score, 1, self.SCORE_COLOR)
        screen.blit(label, self.SCORE_POS)


class Background(GameScreen):

    def __init__(self, game_screen):
        self.gs = game_screen
        self.delay_ms = 150

        self.bg_img = 'images/bg.png'
        self.fence_img = 'images/fence.png'

        self.bg = pygame.image.load(self.bg_img)
        self.fence = pygame.image.load(self.fence_img)

        self.fence_y = self.gs.SCREEN_HEIGHT - 40
        self.fences = [{'x': 0, 'y': self.fence_y}]

    def update_background(self, screen):
        screen.blit(self.bg, (0, 0))

        for fence in self.fences:
            fence['x'] -= 10
            screen.blit(self.fence, (fence['x'], fence['y']))

        fence_w = self.fence.get_width()

        # add fence
        if self.fences[-1]['x'] <= (self.gs.SCREEN_WIDTH + fence_w):
            fence_x = self.fences[-1]['x'] + fence_w
            self.fences.append({'x': fence_x, 'y': self.fence_y})

        # remove fence
        if self.fences[0]['x'] + fence_w < 0:
            self.fences.pop(0)

    def update_display(self):
        pygame.display.flip()
        pygame.time.delay(self.delay_ms)


class Bird(GameScreen):
    def __init__(self, game_screen):
        self.BIRD_INITIAL_ANGLE = 0
        self.BIRD_MAX_UP_ANGLE = 20
        self.BIRD_MAX_DOWN_ANGLE = -90
        self.BIRD_CHANGE_ANGLE = 30
        self.BIRD_INITIAL_YPOS = 200
        self.BIRD_Y = 40
        self.BIRD_XPOS = 50

        self.gs = game_screen
        self.bird_pos = {'x': self.BIRD_XPOS, 'y': self.BIRD_INITIAL_YPOS}
        self.bird_angle = self.BIRD_INITIAL_ANGLE
        self.wing_up = True

        self.bird_img = 'images/bird.png'
        self.bird_up_img = 'images/bird_up.png'
        self.bird_down_img = 'images/bird_down.png'

        self.bird = pygame.image.load(self.bird_img)
        self.bird_up = pygame.image.load(self.bird_up_img)
        self.bird_down = pygame.image.load(self.bird_down_img)

        self.use_bird = None

    def fly(self, screen):
        if self.wing_up:
            self.wing_up = False
            self.use_bird = pygame.transform.rotate(self.bird_up, self.bird_angle)
        else:
            self.wing_up = True
            self.use_bird = pygame.transform.rotate(self.bird_down, self.bird_angle)

        if self.bird_angle <= self.BIRD_MAX_DOWN_ANGLE:
            self.use_bird = pygame.transform.rotate(self.bird, self.bird_angle)

        # bird should not fly beyond fence
        if self.bird_pos['y'] + self.use_bird.get_height() >= self.gs.SCREEN_HEIGHT-40:
            self.bird_pos['y'] = self.gs.SCREEN_HEIGHT-40-self.use_bird.get_height()

        screen.blit(self.use_bird, (self.bird_pos['x'], self.bird_pos['y']))

    def is_hit(self, screen):
        # if bird hits ground
        if self.bird_pos['y'] + self.use_bird.get_height() >= self.gs.SCREEN_HEIGHT - 40:
            return True
        return False

    def fly_up_down(self, screen, key_pressed):
        # if key pressed move bird up
        # else move bird down
        if key_pressed:
            self.bird_pos['y'] -= self.BIRD_Y
            self.bird_angle = self.BIRD_MAX_UP_ANGLE

        else:

            # gradually turn bird down till -90
            # bird falls down in various speed
            if self.bird_angle > self.BIRD_MAX_DOWN_ANGLE:
                self.bird_angle -= self.BIRD_CHANGE_ANGLE
                self.bird_pos['y'] += 10
            else:
                self.bird_angle = self.BIRD_MAX_DOWN_ANGLE
                self.bird_pos['y'] += self.BIRD_Y

        self.fly(screen)


class Pipe(GameScreen):
    def __init__(self, game_screen):
        self.gs = game_screen
        self.DISTANCE = 200
        self.BIRD_HEIGHT = 30
        self.BIRD_VAR = 3
        self.MINHEIGHT = 80
        self.MAXHEIGHT = 320
        self.pipes = []

        self.pipe_img = 'images/pipe.png'
        self.pipe_cup_img = 'images/pipe_cup.png'
        self.pipe = pygame.image.load(self.pipe_img)
        self.pipe_cup = pygame.image.load(self.pipe_cup_img)

    def add_pipe(self):
        # get random heights
        height = random.randrange(self.MINHEIGHT, self.MAXHEIGHT)

        # resize pipe height
        bottom_pipe = pygame.transform.scale(self.pipe, (self.pipe.get_width(), height))

        # resized pipe position on fence
        bottom_pipe_rect = bottom_pipe.get_rect()
        bottom_pipe_rect.bottomleft = (500, self.gs.SCREEN_HEIGHT - 40)

        # pipe cup position on pipe
        bottom_pipe_cup_rect = self.pipe_cup.get_rect()
        bottom_pipe_cup_rect.midtop = bottom_pipe_rect.midtop

        # height of pipe from top
        height = (self.gs.SCREEN_HEIGHT - 40) - height - (self.BIRD_HEIGHT * self.BIRD_VAR)

        # resize top pipe height
        top_pipe = pygame.transform.scale(self.pipe, (self.pipe.get_width(), height))

        # resized pipe position from top
        top_pipe_rect = top_pipe.get_rect()
        top_pipe_rect.left = bottom_pipe_rect.left

        # top pipe cup postion on top pipe
        top_pipe_cup_rect = self.pipe_cup.get_rect()
        top_pipe_cup_rect.midbottom = top_pipe_rect.midbottom

        # add bottom and top pipes
        self.pipes.append({'bottom_pipe': bottom_pipe, 'bottom_pipe_rect': bottom_pipe_rect, 'bottom_pipe_cup_rect': bottom_pipe_cup_rect, 'top_pipe': top_pipe, 'top_pipe_rect': top_pipe_rect, 'top_pipe_cup_rect': top_pipe_cup_rect})

    def update_pipe(self, screen):

        # add pipe
        if not self.pipes or self.pipes[-1]['bottom_pipe_rect'].right <= self.gs.SCREEN_HEIGHT - self.DISTANCE:
            self.add_pipe()

        # remove pipe
        if self.pipes and self.pipes[0]['bottom_pipe_cup_rect'].right < 0:
            del self.pipes[0]

        for pipe in self.pipes:
            pipe['bottom_pipe_rect'].left -= 10
            pipe['bottom_pipe_cup_rect'].left -= 10
            screen.blit(pipe['bottom_pipe'], pipe['bottom_pipe_rect'])
            screen.blit(self.pipe_cup, pipe['bottom_pipe_cup_rect'])

            pipe['top_pipe_rect'].left -= 10
            pipe['top_pipe_cup_rect'].left -= 10
            screen.blit(pipe['top_pipe'], pipe['top_pipe_rect'])
            screen.blit(self.pipe_cup, pipe['top_pipe_cup_rect'])
