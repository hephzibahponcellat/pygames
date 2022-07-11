from flappy_bird import *


def play_game():
    pass


def game_not_started(screen, bg):
    bg.update_background(screen)


def main():
    s = GameScreen()
    bg = Background(s)

    screen = s.create_screen()

    game_running = True
    start_game = False
    while game_running:
        # Get all events
        # Check for Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            # Check for space / mouse press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                start_game = True

        # if yes, start game
        # else just make the bird fly
        if start_game:
            play_game()
        else:
            game_not_started(screen, bg)

        pygame.display.flip()
        pygame.time.delay(250)


if __name__ == '__main__':
    main()
