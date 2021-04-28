from snake_mod import *


def main():

    # screen initialization
    screen = screen_init()

    # initial position for snake with food
    x1y1, x2y2, snake_len, snake_cur_dir = snake_initial_position(screen)
    print(x1y1, x2y2, snake_len, snake_cur_dir)

    # once any arrow key pressed, start the game
    game_on, snake_speed, key_pressed = start_game()
    print(game_on, snake_speed, key_pressed)

    clock = pygame.time.Clock()

    # while game is on
    while game_on:
        clock.tick(snake_speed)

        # move the snake
        x1y1, x2y2 = move_snake(snake_speed, key_pressed, snake_cur_dir,
                                x1y1, x2y2, screen, snake_len)
        print("#", x1y1, x2y2)

        # check if it has hit the wall
        # if yes, end game
        hit_wall = did_hit_wall(x1y1, x2y2)
        if hit_wall:
            game_on = False

        # check if it has hit its own body
        # if yes, end game

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
