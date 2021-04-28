import pygame
import sys


screen_size = 500, 500

colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255)
}

# variables that would change over the game
snake_inc_level = 2
initial_snake_len = 40

# DONT ALTER below variables
snake_body_scales = 10
snake_fat = 8


def screen_init():
    global screen_size, colors

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(colors["BLACK"])
    pygame.display.flip()

    return screen


def snake_initial_position(screen):
    global screen_size, colors, initial_snake_len, snake_fat, snake_body_scales

    snake_current_dir = "right"

    myfont = pygame.font.SysFont("Comic Sans MS", 15)
    message = "Press any arrow key to start the game"
    label = myfont.render(message, 1, colors["GREEN"])
    screen.blit(label, (10, 10))

    x1 = x2 = mid_x_screen_point = screen_size[0]/2
    y1 = y2 = mid_y_screen_point = screen_size[1]/2

    x2 += snake_body_scales

    for x in range(initial_snake_len // snake_body_scales):
        x1 = x1 + snake_body_scales
        x2 = x2 + snake_body_scales

        pygame.draw.line(screen, colors["GREEN"], (x1, y1), (x2, y2), 8)

    pygame.display.flip()

    x1y1 = [mid_x_screen_point, y1]
    x2y2 = [mid_x_screen_point + initial_snake_len, y2]

    return x1y1, x2y2, initial_snake_len, snake_current_dir


def move_snake(snake_speed, key_pressed, snake_cur_dir,
               x1y1, x2y2, screen, snake_len):

    global screen_size, colors, initial_snake_len, snake_fat, snake_body_scales

    screen.fill(colors["BLACK"])

    x1y1[0] = x1y1[0] + snake_body_scales

    x1 = x1y1[0]
    y1 = x1y1[1]

    """
    changing snake direction logic

    if the snake is facing right or left direction
        if right is key_pressed
            no action
        if left is pressed
            no action
        if up is pressed
            move up
        if down is pressed
            move down

    if the snake is facing up or down direction
        if right is pressed
            move right
        if left is pressed
            move left
        if up is pressed
            no action
        if down is pressed
            no action
    """
    print(snake_cur_dir)
    if snake_cur_dir == "right" or snake_cur_dir == "left":
        if key_pressed == "up":
            print("change dir to up")
            snake_cur_dir = "up"

        elif key_pressed == "down":
            print("change dir to down")
            snake_cur_dir = "down"

    elif snake_cur_dir == "up" or snake_cur_dir == "down":
        if key_pressed == "right":
            print("change dir to right")
            snake_cur_dir = "right"

        elif key_pressed == "left":
            print("change dir to left")
            snake_cur_dir = "left"

    for x in range(snake_len // 10):
        x1 = x1 + snake_body_scales
        x2 = x1 + snake_body_scales

        pygame.draw.line(screen, colors["GREEN"], (x1, y1), (x2, y1), 8)

    pygame.display.flip()

    x2y2[0] = x2

    return x1y1, x2y2, snake_cur_dir


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

    if x1y1[0] >= screen_size[0] or x2y2[0] >= screen_size[0] \
       or x1y1[1] >= screen_size[1] or x2y2[1] >= screen_size[1]:
        return True

    if x1y1[0] <= 0 or x2y2[0] <= 0 or x1y1[1] <= 0 or x2y2[1] <= 0:
        return True
