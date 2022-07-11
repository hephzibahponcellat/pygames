from flappy_bird import *


def play_game():
    pass


def game_not_started(screen, bg, bird):
    bg.update_background(screen)
    bird.fly(screen)


def main():
    s = GameScreen()
    bg = Background(s)
    bird = Bird(s)

    screen = s.create_screen()

    game_running = True
    start_game = False
    while game_running:
        # Get all events
        for event in pygame.event.get():
            # Check for Quit event
            if event.type == pygame.QUIT:
                game_running = False

            # Check for space / mouse click
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                start_game = True

        # if space / mouse clicked, start game
        # else just make the bird fly
        if start_game:
            play_game()
        else:
            game_not_started(screen, bg, bird)

        pygame.display.flip()
        pygame.time.delay(250)


if __name__ == '__main__':
    main()
