from flappy_bird import *


def play_game(gs):
    # check if bird hit, yes,
    # blink screen
    # crash bird to ground
    # stop background animation

    if gs.game_over:
        gs.bg.freeze_bg(gs.screen)
        gs.pipe.display(gs.screen)
        gs.bird.fall_down(gs.screen)
        gs.score.final_board(gs.screen)
    else:
        gs.bg.update_background(gs.screen)
        gs.pipe.update_pipe(gs.screen)
        gs.bird.fly_up_down(gs.screen, gs.key_pressed)
        gs.score.display(gs.screen, gs.pipe, gs.bird)

    if gs.bird.is_hit(gs.screen, gs.pipe):
        gs.game_over = True

    if gs.bird.is_bird_ground():
        gs.ready_to_restart = True


def game_not_started(gs):
    gs.bg.update_background(gs.screen)
    gs.bird.fly(gs.screen)


class Game():
    def __init__(self):
        self.s = GameScreen()
        self.bg = Background(self.s)
        self.bird = Bird(self.s)
        self.pipe = Pipe(self.s)
        self.score = Score(self.s)
        self.screen = self.s.create_screen()
        self.start_game = False
        self.key_pressed = False
        self.game_over = False
        self.ready_to_restart = False


def main():
    gs = Game()

    game_running = True
    while game_running:
        gs.key_pressed = False

        # Get all events
        for event in pygame.event.get():
            # Check for Quit event
            if event.type == pygame.QUIT:
                game_running = False

            # Check for space / mouse click
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    gs.start_game = True
                    gs.key_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                gs.start_game = True
                gs.key_pressed = True

        # if space / mouse clicked, start game
        # else just make the bird fly
        if gs.start_game:
            play_game(gs)
        else:
            game_not_started(gs)

        gs.bg.update_display()

        # restart game
        if gs.ready_to_restart and gs.game_over and gs.key_pressed:
            del gs
            gs = Game()


if __name__ == '__main__':
    main()
