from snake_mod import *
import sys


def main():

    # screen initialization
    screen = screen_init()

    # initial position for snake with food
    x1y1, x2y2, snake_len = snake_initial_position(screen)

    # once any arrow key pressed, start the game
    game_on, snake_speed, key_pressed = start_game()
    print(game_on, snake_speed, key_pressed)

    # while game is on
    while game_on:
        # move the snake
        x1y1, x2y2 = move_snake(snake_speed, key_pressed,
                                x1y1, x2y2, screen, snake_len)

        # check if it has hit the wall
        # if yes, end game
        hit_wall = did_hit_wall(x1y1, x2y2)
        print(x1y1, x2y2)
        if hit_wall:
            sys.exit()

        for event in pygame.event.get():
            # if user clicks exit button
            if event.type == pygame.QUIT:
                sys.exit()

            # check if the user pressed any arrow key
                # if yes, turn accordingly

            # check if it has ate the food
                # if yes, add score,
                # grow the snake,
                # create new food

    # update score board


if __name__ == "__main__":
    main()
