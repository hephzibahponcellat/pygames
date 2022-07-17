import pygame
import random
import pickle


class GameScreen():
    def __init__(self):
        self.SCREEN_HEIGHT = 500
        self.SCREEN_WIDTH = 500
        self.CAPTION = 'Flappy Bird'

    def create_screen(self):
        screen = pygame.display.set_mode((self.SCREEN_HEIGHT, self.SCREEN_WIDTH))
        pygame.display.set_caption(self.CAPTION)

        return screen


class Score(GameScreen):
    def __init__(self, game_screen):
        self.gs = game_screen
        self.game_score = 0
        self.IMPACT_FONT = 'impact'
        self.IMPACT_FONT_SIZE = 40

        self.FINAL_BOARD_SIZE = 30
        self.SCORE_POS = (250, 100)
        self.SCORE_COLOR = (255, 255, 0)
        self.BOARD_COLOR = (235, 52, 91)
        self.BOARD_BG_COLOR = (0, 0, 0)

        pygame.font.init()
        self.score = pygame.font.SysFont(self.IMPACT_FONT, self.IMPACT_FONT_SIZE)

        self.board = pygame.font.SysFont(self.IMPACT_FONT, self.FINAL_BOARD_SIZE)

    def display(self, screen):
        score = str(self.game_score)
        label = self.score.render(score, 1, self.SCORE_COLOR)
        screen.blit(label, self.SCORE_POS)

    def display_multiline(self, screen, text):
        lines = text.splitlines()
        label_rect = None

        # find lengthiest line
        longest_line = max(lines, key=len)
        label = self.board.render(longest_line, 1, self.SCORE_COLOR)
        max_size = (label.get_width() + 40, label.get_height() + 10)

        # fill bg color
        temp_surface = pygame.Surface((max_size))
        label_rect = temp_surface.get_rect()
        label_rect.center = (self.gs.SCREEN_WIDTH//2, 150)

        for i, line in enumerate(lines):
            # toggle color
            if (i + 1) % 2 == 0:
                text = self.board.render(line, 1, self.SCORE_COLOR)
            else:
                text = self.board.render(line, 1, self.BOARD_COLOR)

            if i:
                label_rect.midtop = label_rect.midbottom

            w = (label_rect.w - text.get_width()) // 2
            temp_surface.fill(self.BOARD_BG_COLOR)
            temp_surface.blit(text, (w, 10))
            screen.blit(temp_surface, (label_rect))

    def final_board(self, screen):
        text = 'SCORE\n' + str(self.game_score)

        # find best score
        try:
            fp = open('.best_score.pickle', 'rb')
        except FileNotFoundError:
            best_score = self.game_score
        else:
            best_score = pickle.load(fp)
            if self.game_score > best_score:
                best_score = self.game_score
            fp.close()

        # write best score to tmp file
        with open('.best_score.pickle', 'wb') as fp:
            pickle.dump(best_score, fp)

        text += '\nBEST\n' + str(best_score)
        text += '\nSPACE to Retry'

        self.display_multiline(screen, text)


class Background(GameScreen):

    def __init__(self, game_screen):
        self.WHITE = (255, 255, 255)

        self.gs = game_screen
        self.delay_ms = 150
        self.blink = True

        self.bg_img = 'images/bg.png'
        self.fence_img = 'images/fence.png'

        self.bg = pygame.image.load(self.bg_img)
        self.fence = pygame.image.load(self.fence_img)

        self.fence_y = self.gs.SCREEN_HEIGHT - 40
        self.fences = [{'x': 0, 'y': self.fence_y}]

    def freeze_bg(self, screen):
        if self.blink:
            screen.fill(self.WHITE)
            self.update_display()
            self.blink = False

        self.update_display(delay_ms=0)
        self.display_bg(screen)

    def display_bg(self, screen):
        screen.blit(self.bg, (0, 0))

        for fence in self.fences:
            screen.blit(self.fence, (fence['x'], fence['y']))

    def update_background(self, screen):

        for fence in self.fences:
            fence['x'] -= 10

        self.display_bg(screen)

        fence_w = self.fence.get_width()

        # add fence
        if self.fences[-1]['x'] <= (self.gs.SCREEN_WIDTH + fence_w):
            fence_x = self.fences[-1]['x'] + fence_w
            self.fences.append({'x': fence_x, 'y': self.fence_y})

        # remove fence
        if self.fences[0]['x'] + fence_w < 0:
            self.fences.pop(0)

    def update_display(self, delay_ms=None):

        if delay_ms is None:
            delay_ms = self.delay_ms

        pygame.display.flip()
        pygame.time.delay(delay_ms)


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

        self.use_bird = self.bird
        self.bird_rect = self.use_bird.get_rect()

    def display(self, screen):
        screen.blit(self.use_bird, self.bird_rect)

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

        self.bird_rect = self.use_bird.get_rect()
        self.bird_rect.topleft = (self.bird_pos['x'], self.bird_pos['y'])

        self.display(screen)

    def is_bird_ground(self):
        if self.bird_pos['y'] == self.gs.SCREEN_HEIGHT-40-self.use_bird.get_height():
            return True
        return False

    def is_hit(self, screen, pipe):
        # if bird hits ground
        if self.bird_pos['y'] + self.use_bird.get_height() >= self.gs.SCREEN_HEIGHT - 40:
            return True

        # if bird hits pipe
        if pipe.pipes:

            # if bird hits top pipe
            top_pipe_rect = pipe.pipes[0]['top_pipe_rect']
            top_pipe_cup_rect = pipe.pipes[0]['top_pipe_cup_rect']

            if self.bird_rect.colliderect(top_pipe_rect):
                return True

            if self.bird_rect.colliderect(top_pipe_cup_rect):
                return True

            # if bird flies top and hit top pipe outside game window
            imaginary_rect = pygame.Rect(top_pipe_rect.topleft, top_pipe_rect.size)
            if self.bird_rect.y < 0:
                imaginary_rect.height = abs(self.bird_rect.y)
            imaginary_rect.bottom = top_pipe_rect.top
            if self.bird_rect.colliderect(imaginary_rect):
                return True

            # if bird hits bottom pipe
            bottom_pipe_rect = pipe.pipes[0]['bottom_pipe_rect']
            bottom_pipe_cup_rect = pipe.pipes[0]['bottom_pipe_cup_rect']

            if self.bird_rect.colliderect(bottom_pipe_rect):
                return True

            if self.bird_rect.colliderect(bottom_pipe_cup_rect):
                return True

        return False

    def fly_up(self):
        self.bird_pos['y'] -= self.BIRD_Y
        self.bird_angle = self.BIRD_MAX_UP_ANGLE

    def fly_down(self):
        # gradually turn bird down till -90
        # bird falls down in various speed
        if self.bird_angle > self.BIRD_MAX_DOWN_ANGLE:
            self.bird_angle -= self.BIRD_CHANGE_ANGLE
            self.bird_pos['y'] += 20
        else:
            self.bird_angle = self.BIRD_MAX_DOWN_ANGLE
            self.bird_pos['y'] += self.BIRD_Y

    def fall_down(self, screen):
        # if bird is top out of game window, set y to 0
        if self.bird_pos['y'] < 0:
            self.bird_pos['y'] = 0

        self.fly_down()
        self.fly(screen)

    def fly_up_down(self, screen, key_pressed):

        # if key pressed move bird up
        # else move bird down
        if key_pressed:
            self.fly_up()
        else:
            self.fly_down()

        self.fly(screen)


class Pipe(GameScreen):
    def __init__(self, game_screen):
        self.gs = game_screen
        self.DISTANCE = 200
        self.BIRD_HEIGHT = 30
        self.BIRD_VAR = 4.5
        self.MINHEIGHT = 80
        self.MAXHEIGHT = (self.gs.SCREEN_HEIGHT - 40) - self.MINHEIGHT - (self.BIRD_HEIGHT * self.BIRD_VAR)
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

    def display(self, screen):
        for pipe in self.pipes:
            screen.blit(pipe['bottom_pipe'], pipe['bottom_pipe_rect'])
            screen.blit(self.pipe_cup, pipe['bottom_pipe_cup_rect'])
            screen.blit(pipe['top_pipe'], pipe['top_pipe_rect'])
            screen.blit(self.pipe_cup, pipe['top_pipe_cup_rect'])

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

            pipe['top_pipe_rect'].left -= 10
            pipe['top_pipe_cup_rect'].left -= 10

        self.display(screen)
