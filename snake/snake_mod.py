import pygame
from time import sleep


screen_size = 500, 500
snake_inc_level = 0.1

initial_snake_len = 50
snake_fat = 8

# colors
colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0)
}


def screen_init():
    global screen_size, colors

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(colors["BLACK"])
    pygame.display.flip()

    return screen


def snake_initial_position(screen):
    global screen_size, colors, initial_snake_len, snake_fat

    mid_x_screen_point = screen_size[0]/2
    mid_y_screen_point = screen_size[1]/2

    x1y1 = [mid_x_screen_point, mid_y_screen_point]
    x2y2 = [mid_x_screen_point - initial_snake_len, mid_y_screen_point]

    snake = pygame.draw.line(screen, colors["GREEN"], x1y1, x2y2, snake_fat)
    pygame.display.flip()

    return x1y1, x2y2, initial_snake_len


def move_snake(snake_speed, key_pressed, x1y1, x2y2, screen, snake_len):

    global screen_size, colors, initial_snake_len, snake_fat

    screen.fill(colors["BLACK"])

    x1y1[0] = x1y1[0] + snake_speed
    x2y2[0] = x2y2[0] + snake_speed

    pygame.draw.line(screen, colors["GREEN"], x1y1, x2y2, snake_fat)
    pygame.display.flip()

    return x1y1, x2y2


def start_game():
    global snake_inc_level
    game_on = False
    snake_speed = 0
    key_pressed = ""

    while not game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    key_pressed = "right"
                elif event.key == pygame.K_LEFT:
                    key_pressed = "left"
                elif event.key == pygame.K_UP:
                    key_pressed = "up"
                elif event.key == pygame.K_DOWN:
                    key_pressed = "down"

                if key_pressed:
                    game_on = True
                    snake_speed += snake_inc_level

                    return game_on, snake_speed, key_pressed


def did_hit_wall(x1y1, x2y2):
    global screen_size

    if x1y1[0] > screen_size[0] or x2y2[0] > screen_size[0] \
       or x1y1[1] > screen_size[1] or x2y2[1] > screen_size[1]:
        return True

    if x1y1[0] < 0 or x2y2[0] < 0 or x1y1[1] < 0 or x2y2[1] < 0:
        return True
