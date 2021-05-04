from snake_mod import *


def main():
    score = 0

    # screen initialization
    screen = screen_init()

    food_pos = create_food(screen)

    # initial position for snake with food
    snake_cur_dir, snake_scale_positions = snake_initial_position(screen)

    # once any arrow key pressed, start the game
    game_on, key_pressed = start_game()
    print(game_on, snake_speed, key_pressed)

    clock = pygame.time.Clock()

    # while game is on
    while game_on:
        clock.tick(snake_speed)

        # clear the screen
        clear_screen(screen)

        # draw the existing snake_food
        create_food(screen, food_pos)

        # move the snake
        snake_cur_dir,\
        snake_scale_positions = move_snake(key_pressed,
                                           snake_cur_dir,
                                           screen,
                                           snake_scale_positions)
        key_pressed = ""

        # check if it has hit the wall
        # if yes, end game
        hit_wall = did_hit_wall(snake_scale_positions)
        if hit_wall:
            game_on = False

        # check if it has hit its own body
        # if yes, end game
        bite_itself = did_bite_itself(snake_scale_positions)
        if bite_itself:
            game_on = False

        # check if it has ate the food
        # if yes, add score, grow the snake, create new food
        ate_food = check_if_ate_food(food_pos, snake_scale_positions)
        if ate_food:
            snake_scale_positions.insert(0, snake_scale_positions[0])
            food_pos = create_food(screen)
            score += 10

        # write score board to the game screen
        write_score(screen, score)

        # update the screen
        update_screen()

        for event in pygame.event.get():
            # if user clicks exit button
            if event.type == pygame.QUIT:
                sys.exit()

            # check if the user pressed any arrow key
                # if yes, turn accordingly
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    key_pressed = "right"
                elif event.key == pygame.K_LEFT:
                    key_pressed = "left"
                elif event.key == pygame.K_UP:
                    key_pressed = "up"
                elif event.key == pygame.K_DOWN:
                    key_pressed = "down"


if __name__ == "__main__":
    main()
