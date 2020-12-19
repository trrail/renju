import pygame
from renju.game import game, player, bot
from renju.game.color import Color


def mouse_click_is_correct(mouse_position: tuple) -> bool:
    # Checking, that mouse on game board
    if 25 <= mouse_position[0] <= 395 and 25 <= mouse_position[1] <= 395:
        return True
    return False


def define_position() -> tuple:
    if pygame.mouse.get_pressed(3)[0]:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_click_is_correct(mouse_pos):
            x_whole = (mouse_pos[0] - 9) // 25 - 1
            x_residue = (mouse_pos[0] - 9) % 25
            y_whole = (mouse_pos[1] - 9) // 25 - 1
            y_residue = (mouse_pos[1] - 9) % 25
            x_pos = x_whole if x_residue < 12 else x_whole + 1
            y_pos = y_whole if y_residue < 12 else y_whole + 1
            return x_pos, y_pos


class Window:
    def __init__(self):
        self.current_condition = self.open_menu
        self.screen_size = (700, 470)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bg_game_screen = pygame.image.load("resources/board.png")
        self.winner_color = None
        self.hard_mode_bot = False
        self.chip_radius = 10
        self.players_count = 0
        self.bots_count = 0
        self.game = game.Game()

        # На будующее ;)
        self.mode_bots_count = 0
        self.pointer = 0

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
        self.print_text("P - play",
                        (10, self.screen_size[1] / 2 + 30), 34)
        self.print_text("T - high score",
                        (10, self.screen_size[1] / 2 + 60), 34)
        if pygame.key.get_pressed()[pygame.K_p]:
            self.current_condition = self.select_bot_and_player_count_menu
        if pygame.key.get_pressed()[pygame.K_t]:
            self.current_condition = self.high_score_table_screen

    def select_bot_and_player_count_menu(self):
        self.reset_settings()
        # Разделение на выбор колличества ботов и игроков
        type_of_player = "игроков" if self.pointer == 0 else "ботов"

        # Кнопка меню
        self.print_text("M - menu", (self.screen_size[0] / 2 - 65,
                                     self.screen_size[1] - 35), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.winner_color = None
            self.current_condition = self.open_menu

        # Текст
        self.print_text(
            "Выберите кол-во"
            + type_of_player
            + ". Макс. кол-во: "
            + str(9 - self.players_count - self.bots_count),
            (self.screen_size[0] / 2 - 240, 100),
            34,
        )

        # Выбранное количество
        self.print_text(
            str(self.bots_count if self.pointer == 1 else self.players_count),
            (self.screen_size[0] / 2 - 35, 160),
            100,
        )

        # Кнопка продолжения
        self.print_text(
            "N - next", (self.screen_size[0] - 100,
                         self.screen_size[1] - 35), 34
        )
        if pygame.key.get_pressed()[pygame.K_n]:
            pygame.time.wait(100)
            if self.pointer == 1 and self.players_count + self.bots_count > 1:
                self.pointer = 0
                if self.bots_count > 0:
                    self.current_condition = self.choose_bot_level_screen
                else:
                    self.game.prepare_game(self.prepare_players())
                    self.current_condition = self.game_window
            elif self.pointer != 1:
                self.pointer += 1

        # Кнопка отката
        self.print_text("R - return", (10, self.screen_size[1] - 35), 34)
        if pygame.key.get_pressed()[pygame.K_r]:
            pygame.time.wait(100)
            if self.pointer == 0:
                self.current_condition = self.open_menu
            else:
                self.pointer -= 1

        # Кнопка прибавления
        self.print_text(
            "+", (self.screen_size[0] / 2 + 40, self.screen_size[1] / 2), 80
        )
        if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            pygame.time.wait(200)
            if self.players_count + self.bots_count != 9:
                if self.pointer == 0:
                    self.players_count += 1
                else:
                    self.bots_count += 1

        # Кнопка уменьшения
        self.print_text(
            "-", (self.screen_size[0] / 2 - 100, self.screen_size[1] / 2), 80
        )
        if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
            pygame.time.wait(100)
            if self.pointer == 0 and self.players_count > 0:
                self.players_count -= 1
            elif self.bots_count > 0:
                self.bots_count -= 1

    def game_window(self) -> None:
        self.reset_settings()
        self.prepare_game_screen()
        self.print_moves()
        self.update_screen()
        self.print_text("M - menu", (10, self.screen_size[1] - 35), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = self.open_menu
        pos = self.game.take_pos()
        if pos is not None:
            self.winner_color = self.game.make_move(pos)
            pygame.time.wait(100)
        if self.winner_color is not None or self.game.chips_count == 225:
            self.current_condition = self.game_over

    def game_over(self) -> None:
        self.reset_settings()
        if self.winner_color is not None:
            self.print_text(
                "is Winner",
                (self.screen_size[0] // 2 - 40, self.screen_size[1] // 2 - 10),
                34,
            )
            pygame.draw.circle(
                self.screen,
                self.winner_color,
                (self.screen_size[0] // 2 - 70, self.screen_size[1] // 2),
                20,
            )
        elif self.winner_color is None:
            self.print_text(
                "Draw",
                (self.screen_size[0] // 2 - 40, self.screen_size[1] // 2 - 10),
                34,
            )
        self.print_text("M - menu", (10, self.screen_size[1] - 40), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.winner_color = None
            self.current_condition = self.open_menu
        self.print_text("T - high score", (150, self.screen_size[1] - 40), 34)
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
        self.print_text(
            "Выберите сложность бота",
            (self.screen_size[0] / 2 - 195, self.screen_size[1] / 2 - 50),
            45,
        )
        self.print_text("M - menu", (10, self.screen_size[1] - 40), 34)
        self.print_text("H - сложный", (self.screen_size[0] / 2 - 160,
                                        self.screen_size[1] / 2), 34)
        self.print_text("E - лёгкий", (self.screen_size[0] / 2 + 30,
                                       self.screen_size[1] / 2), 34)
        if pygame.key.get_pressed()[pygame.K_m]:
            self.current_condition = self.open_menu
        if pygame.key.get_pressed()[pygame.K_h]:
            self.hard_mode_bot = True
            self.game.prepare_game(self.prepare_players())
            self.current_condition = self.game_window
        if pygame.key.get_pressed()[pygame.K_e]:
            self.hard_mode_bot = False
            self.game.prepare_game(self.prepare_players())
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
        self.print_text(f'Времени осталось: {self.game.time_left}   '
                        f'Ходит: ', (220, self.screen_size[1] - 35), 34)
        self.draw_chip(
            self.game.get_current_player_color(), (23, 16.5), 15, self.screen
        )

    def print_text(self, message: str, position: tuple, font: int) -> None:
        text_stile = pygame.font.Font(None, font)
        text = text_stile.render(message, True, (255, 255, 255))
        self.screen.blit(text, position)

    def update_screen(self) -> None:
        # Re-draw game map with new chips
        for x in range(self.game.map.width):
            for y in range(self.game.map.height):
                if self.game.map.map[x][y]:
                    chip = self.game.map.map[x][y]
                    self.draw_chip(chip, (x, y), self.chip_radius, self.screen)

    def print_moves(self) -> None:
        # Print log
        x_pos = 475
        y_pos = 10
        for move in self.game.moves:
            pygame.draw.circle(self.screen, move[0], (457, y_pos + 6), 10)
            self.print_text(
                "поставил(-ла) в клетку ("
                + str(move[1][0])
                + ", "
                + str(move[1][1])
                + ")",
                (x_pos, y_pos),
                23,
            )
            self.print_text(str(move[2]) + ".", (425, y_pos), 23)
            y_pos += 30

    def print_high_score_table(self):
        x_pos = self.screen_size[0] / 2 - 80
        y_pos = 70
        statistic = self.game.get_statistic()
        self.print_text("Игроки" + "  " * 4 +
                        "Победы", (x_pos - 50, y_pos - 50), 40)
        for key in statistic.keys():
            combo = key.split(", ")
            color = (
                int(combo[0][1::]),
                int(combo[1]),
                int(combo[2][:len(combo[2]) - 1:]),
            )
            pygame.draw.circle(self.screen, color, (x_pos, y_pos + 10), 20)
            self.print_text(str(statistic.get(key)), (x_pos + 150, y_pos), 40)
            y_pos += 50

    @staticmethod
    def draw_chip(color: tuple, position: tuple,
                  radius: float, surface: pygame.Surface) -> None:
        position = ((position[0] + 1) * 25 + 9, (position[1] + 1) * 25 + 9)
        pygame.draw.circle(surface, color, position, radius)

    def prepare_players(self) -> list:
        players = []
        colors = list(Color)
        for gamer in range(self.players_count):
            players.append(player.Player(colors.pop(0).value,
                                         callback=define_position))
        for bot_player in range(self.bots_count):
            players.append(
                bot.HardModeBot(colors.pop(0).value, callback=None)
                if self.hard_mode_bot
                else bot.EasyModeBot(colors.pop(0).value, callback=None)
            )

        return players
