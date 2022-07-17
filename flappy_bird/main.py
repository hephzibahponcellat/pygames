from flappy_bird import *


def play_game(screen, bg, bird, pipe, score, key_pressed):
    # check if bird hit, yes,
    # blink screen
    # crash bird to ground
    # stop background animation
    if bird.is_hit(screen, pipe):
        score.game_over = True

    if score.game_over:
        bg.freeze_bg(screen)
        pipe.display(screen)
        bird.fall_down(screen)
        score.final_board(screen)
    else:
        bg.update_background(screen)
        pipe.update_pipe(screen)
        bird.fly_up_down(screen, key_pressed)
        score.display(screen)


def game_not_started(screen, bg, bird, score):
    bg.update_background(screen)
    bird.fly(screen)


def main():
    s = GameScreen()
    bg = Background(s)
    bird = Bird(s)
    pipe = Pipe(s)
    score = Score(s)

    screen = s.create_screen()

    game_running = True
    start_game = False
    while game_running:
        key_pressed = False

        # Get all events
        for event in pygame.event.get():
            # Check for Quit event
            if event.type == pygame.QUIT:
                game_running = False

            # Check for space / mouse click
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    start_game = True
                    key_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                start_game = True
                key_pressed = True

        # if space / mouse clicked, start game
        # else just make the bird fly
        if start_game:
            play_game(screen, bg, bird, pipe, score, key_pressed)
        else:
            game_not_started(screen, bg, bird, score)

        bg.update_display()


if __name__ == '__main__':
    main()
