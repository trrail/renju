import pygame
from game import game


class Window:
    def __init__(self):
        self.current_condition = self.open_menu
        self.screen_size = (420, 470)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bg_game_screen = pygame.image.load('board.png')
        self.game = None
        self.winner_color = None

    def start(self) -> None:
        pygame.init()
        window_is_open = True
        while window_is_open:
            self.current_condition()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window_is_open = False
            pygame.display.update()
        pygame.quit()

    def open_menu(self) -> None:
        self.return_default_settings()
        self.print_text("Renju", (18, 25), 70)
        self.print_text("P - 2 players", (10, self.screen_size[1] / 2 + 30), 34)
        self.print_text("B - bot", (10, self.screen_size[1] / 2), 34)
        if pygame.key.get_pressed()[pygame.K_p]:
            self.game = game.Game(False)
            self.current_condition = self.game_window
        if pygame.key.get_pressed()[pygame.K_b]:
            self.game = game.Game(True)
            self.current_condition = self.game_window

    def game_window(self) -> None:
        self.screen.blit(self.bg_game_screen, (0, 0))
        self.update_screen()
        self.print_text("M - menu", (10, self.screen_size[1] - 35), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = self.open_menu
        mouse_pos = pygame.mouse.get_pos()
        mouse_is_pressed = pygame.mouse.get_pressed(3)[0]
        pos = self.game.take_pos()
        if mouse_is_pressed:
            if pos is None and self.mouse_click_is_correct(mouse_pos):
                self.winner_color = self.game.make_move(self.define_position(mouse_pos))
        if pos is not None:
            self.winner_color = self.game.make_move(pos)
        if self.winner_color is not None or self.game.chips_count == 225:
            self.current_condition = self.game_over

    def game_over(self) -> None:
        self.return_default_settings()
        if self.winner_color is not None:
            self.print_text("is Winner", (self.screen_size[0] // 2 - 40, self.screen_size[1] // 2 - 10), 34)
            pygame.draw.circle(self.screen, self.winner_color,
                               (self.screen_size[0] // 2 - 70, self.screen_size[1] // 2), 20)
        elif self.winner_color is None:
            self.print_text("Draw", (self.screen_size[0] // 2 - 40, self.screen_size[1] // 2 - 10), 34)
        self.print_text("M - menu", (10, self.screen_size[1] - 40), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.winner_color = None
            self.current_condition = self.open_menu

    def return_default_settings(self) -> None:
        surface = pygame.Surface((420, 470))
        surface.fill((255, 165, 0))
        self.screen.blit(surface, (0, 0))

    def print_text(self, message: str, position: tuple, font: int) -> None:
        text_stile = pygame.font.Font(None, font)
        text = text_stile.render(message, True, (255, 255, 255))
        self.screen.blit(text, position)

    def update_screen(self) -> None:
        for x in range(self.game.map.width):
            for y in range(self.game.map.height):
                if self.game.map.map[x][y]:
                    self.game.map.map[x][y].draw_chip(self.screen)

    @staticmethod
    def define_position(mouse_pos: tuple) -> tuple:
        # При нажатии мыши определяет текущее положение на игровой карте
        x_whole = (mouse_pos[0] - 9) // 25 - 1
        x_residue = (mouse_pos[0] - 9) % 25
        y_whole = (mouse_pos[1] - 9) // 25 - 1
        y_residue = (mouse_pos[1] - 9) % 25
        x_pos = x_whole if x_residue < 12 else x_whole + 1
        y_pos = y_whole if y_residue < 12 else y_whole + 1
        return x_pos, y_pos

    @staticmethod
    def mouse_click_is_correct(mouse_position: tuple) -> bool:
        if 25 <= mouse_position[0] <= 395 and 25 <= mouse_position[1] <= 395:
            return True
        return False
