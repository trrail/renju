import pygame
from GAME import Game


class Window():
    def __init__(self):
        self.conditions = [self.open_menu,
                           self.game_window,
                           self.gameover]
        self.current_condition = 0
        self.screen_size = (420, 470)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bg_game_screen = pygame.image.load('Core/board.png')
        self.game = None
        self.winner_color = None

    def start(self):
        pygame.init()
        open = True
        while open:
            self.conditions[self.current_condition]()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    open = False
            pygame.display.update()
        pygame.quit()

    def open_menu(self):
        self.return_default_settings()
        self.print_text("Renju", (18, 25), 70)
        self.print_text("P - 2 players", (10, self.screen_size[1] / 2 + 30), 34)
        self.print_text("B - bot", (10, self.screen_size[1] / 2), 34)
        if pygame.key.get_pressed()[pygame.K_p]:
            self.game = Game.Game(False)
            self.current_condition = 1
        if pygame.key.get_pressed()[pygame.K_b]:
            self.game = Game.Game(True)
            self.current_condition = 1

    def game_window(self):
        self.screen.blit(self.bg_game_screen, (0, 0))
        self.update_screen()
        self.print_text("M - menu", (10, self.screen_size[1] - 35), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = 0
        mouse_pos = pygame.mouse.get_pos()
        mouse_is_pressed = pygame.mouse.get_pressed()
        if mouse_is_pressed[0]:
            if 25 <= mouse_pos[0] <= 395 and 25 <= mouse_pos[1] <= 395:
                winner = self.game.make_move()
                if winner is not None:
                    self.winner_color = winner
                    self.current_condition = 2


    def gameover(self):
        pass

    def return_default_settings(self):
        surface = pygame.Surface((420, 470))
        surface.fill((255, 165, 0))
        self.screen.blit(surface, (0, 0))
        self.color = (0, 0, 0)

    def print_text(self, message, position, font):
        text_stile = pygame.font.Font(None, font)
        text = text_stile.render(message, 1, (255, 255, 255))
        self.screen.blit(text, position)

    def update_screen(self):
        pass