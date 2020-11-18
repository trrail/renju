import pygame
from renju.game import game


class Window:
    def __init__(self):
        self.current_condition = self.open_menu
        self.screen_size = (700, 470)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bg_game_screen = pygame.image.load('board.png')
        self.game = game.Game()
        self.winner_color = None
        self.bot_level = None

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
        self.reset_settings()
        self.print_text("renju", (18, 25), 70)
        self.print_text("P - 2 players",
                        (10, self.screen_size[1] / 2 + 30), 34)
        self.print_text("B - bot",
                        (10, self.screen_size[1] / 2), 34)
        self.print_text("T - high score",
                        (10, self.screen_size[1] / 2 + 60), 34)
        if pygame.key.get_pressed()[pygame.K_p]:
            self.game.prepare_game(2, 0)
            self.current_condition = self.game_window
        if pygame.key.get_pressed()[pygame.K_b]:
            self.game.prepare_game(1, 1)
            self.current_condition = self.choose_bot_level_screen
        if pygame.key.get_pressed()[pygame.K_t]:
            self.current_condition = self.high_score_table_screen

        # Это пробный режим для личного использования)
        if pygame.key.get_pressed()[pygame.K_f]:
            self.game.prepare_game(0, 2)
            self.current_condition = self.game_window

    def select_player_menu(self) -> None:
        self.reset_settings()

    def game_window(self) -> None:
        self.reset_settings()
        self.prepare_game_screen()
        self.print_moves()
        self.update_screen()
        self.print_text("M - menu", (10, self.screen_size[1] - 35), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = self.open_menu
        mouse_pos = pygame.mouse.get_pos()
        mouse_is_pressed = pygame.mouse.get_pressed(3)[0]
        pos = self.game.take_pos(self.bot_level)
        if mouse_is_pressed:
            if pos is None and self.mouse_click_is_correct(mouse_pos):
                self.winner_color \
                    = self.game.make_move(self.define_position(mouse_pos))
        if pos is not None:
            self.winner_color = self.game.make_move(pos)
            pygame.time.wait(100)
        if self.winner_color is not None or self.game.chips_count == 225:
            self.current_condition = self.game_over

    def game_over(self) -> None:
        self.reset_settings()
        if self.winner_color is not None:
            self.print_text("is Winner", (self.screen_size[0] // 2 - 40,
                                          self.screen_size[1] // 2 - 10), 34)
            pygame.draw.circle(self.screen, self.winner_color,
                               (self.screen_size[0] // 2 - 70,
                                self.screen_size[1] // 2), 20)
        elif self.winner_color is None:
            self.print_text("Draw",
                            (self.screen_size[0] // 2 - 40,
                             self.screen_size[1] // 2 - 10), 34)
        self.print_text("M - menu",
                        (10, self.screen_size[1] - 40), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.winner_color = None
            self.current_condition = self.open_menu
        self.print_text("T - high score",
                        (150, self.screen_size[1] - 40), 34)
        if pygame.key.get_pressed()[pygame.K_t]:
            self.winner_color = None
            self.current_condition = self.high_score_table_screen

    def high_score_table_screen(self) -> None:
        self.reset_settings()
        self.print_text("M - menu", (10, self.screen_size[1] - 40), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = self.open_menu
        self.print_high_score_table()

    def choose_bot_level_screen(self) -> None:
        self.reset_settings()
        self.print_text("Выберите сложность бота",
                        (self.screen_size[0] / 2 - 195,
                         self.screen_size[1] / 2 - 50), 45)
        self.print_text("M - menu",
                        (10, self.screen_size[1] - 40), 34)
        self.print_text("H - сложный",
                        (self.screen_size[0] / 2 - 160,
                         self.screen_size[1] / 2), 34)
        self.print_text("E - лёгкий",
                        (self.screen_size[0] / 2 + 30,
                         self.screen_size[1] / 2), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = self.open_menu
        if pygame.key.get_pressed()[pygame.K_h]:
            self.bot_level = 1
            self.current_condition = self.game_window
        if pygame.key.get_pressed()[pygame.K_e]:
            self.bot_level = 0
            self.current_condition = self.game_window

    def reset_settings(self) -> None:
        surface = pygame.Surface(self.screen_size)
        surface.fill((255, 165, 0))
        self.screen.blit(surface, (0, 0))

    def prepare_game_screen(self) -> None:
        self.screen.blit(self.bg_game_screen, (0, 0))
        surface = pygame.Surface((280, 420))
        surface.fill((128, 128, 128))
        self.screen.blit(surface, (420, 0))

    def print_text(self, message: str,
                   position: tuple, font: int) -> None:
        text_stile = pygame.font.Font(None, font)
        text = text_stile.render(message, True, (255, 255, 255))
        self.screen.blit(text, position)

    def update_screen(self) -> None:
        # Re-draw game map with new chips
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
        # Checking, that mouse on game board
        if 25 <= mouse_position[0] <= 395 \
                and 25 <= mouse_position[1] <= 395:
            return True
        return False

    def print_moves(self) -> None:
        # Print log
        x_pos = 475
        y_pos = 10
        for move in self.game.moves:
            pygame.draw.circle(self.screen, move[0], (457, y_pos + 6), 10)
            self.print_text('поставил(-ла) в клетку (' +
                            str(move[1][0]) + ', ' + str(move[1][1]) + ')',
                            (x_pos, y_pos), 23)
            self.print_text(str(move[2]) + '.', (425, y_pos), 23)
            y_pos += 30

    def print_high_score_table(self):
        x_pos = self.screen_size[0] / 2 - 80
        y_pos = self.screen_size[1] / 2
        statistic = self.game.get_statistic()
        self.print_text('Игроки' + '  ' * 4 + 'Победы',
                        (x_pos - 50, y_pos - 50), 40)
        for key in statistic.keys():
            color = (0, 0, 0) if key == '(0, 0, 0)' else (255, 255, 255)
            pygame.draw.circle(self.screen, color, (x_pos, y_pos + 10), 20)
            self.print_text(str(statistic.get(key)), (x_pos + 150, y_pos), 40)
            y_pos += 50
