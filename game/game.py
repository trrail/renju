from game import player
from game import bot
from game import map
from game import const
from game import statistic


class Game:
    def __init__(self):
        self.players = []
        self.map = map.Map()
        self.chips_count = 0
        self.current_player = 0
        self.moves = []
        self.winner_size = []
        self.statistic = statistic.Statistic()

    def take_pos(self):
        # Вернёт:
        # - None, если Player
        # - Tuple, если Bot
        return self.players[self.current_player].make_move()

    def make_move(self, position: tuple):
        if self.map.point_is_free(position):
            color = self.players[self.current_player].color
            winner = self.check_winner(position, color)
            if self.check_game_rule(color):
                self.update_game(color, position)
            return winner

    def check_winner(self, position: tuple, color: tuple):
        self.winner_size.clear()
        for direction in const.directions:
            self.winner_size.append(self.map.check_winner(position[0], position[1], direction, color, 1))
        self.winner_size.sort(reverse=True)
        if self.winner_size[0] == 5:
            self.statistic.update_player(color)
            return color

    def add_move_in_stat(self, color, position):
        if len(self.moves) == 14:
            self.moves.pop(0)
        self.moves.append((color, position, self.chips_count))

    def check_game_rule(self, color: tuple) -> bool:
        if color == (0, 0, 0):
            if self.winner_size[0] > 5:
                return False
            if self.winner_size[0] >= 3 and self.winner_size[1] >= 3:
                return False
        return True

    def update_game(self, color: tuple, position: tuple) -> None:
        self.current_player = (self.current_player + 1) % len(self.players)
        self.map.put_chip(color, position)
        self.chips_count += 1
        self.add_move_in_stat(color, position)

    def prepare_game(self, players_count: int, bot_counts: int) -> None:
        self.reset_game()
        color = (0, 0, 0)
        for gamer in range(players_count):
            self.players.append(player.Player(color))
            color = (255, 255, 255)
        for bot_player in range(bot_counts):
            self.players.append(bot.Bot(color))
            color = (255, 255, 255)

    def reset_game(self):
        self.players.clear()
        self.map.map.clear()
        self.map.prepare_map()
        self.chips_count = 0
        self.current_player = 0

    def get_statistic(self):
        return self.statistic.high_score_table
