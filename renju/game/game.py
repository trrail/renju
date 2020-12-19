from renju.game import map, statistic, const
from renju.game.timer import Timer
from renju.game.vector import Vector


class Game:
    def __init__(self):
        self.game_timer = Timer()
        self.players = []
        self.map = map.Map()
        self.chips_count = 0
        self.current_player = 0
        self.moves = []
        self.winner_size = []
        self.statistic = statistic.Statistic()

    def take_pos(self) -> tuple:
        self.game_timer.update_timer(self.update_game_pointer)
        return self.players[self.current_player]\
            .make_move(self.map, len(self.players))

    def make_move(self, position: tuple):
        if self.map.point_is_free(position):
            color = self.players[self.current_player].color
            winner = self.check_winner(position, color)
            if self.map.check_game_rule(color, self.winner_size):
                self.update_game(color, position)
            return winner

    def check_winner(self, position: tuple, color: tuple):
        self.winner_size.clear()
        for direction in const.directions:
            self.winner_size.append(
                self.map.check_winner(Vector((position[0], position[1])),
                                      Vector(direction), color, 1)
            )
        self.winner_size.sort(reverse=True)
        if self.winner_size[0] == 5 and self.map.check_game_rule(
            color, self.winner_size
        ):
            self.statistic.update_player(color)
            return color

    def add_move_in_stat(self, color: tuple, position: tuple) -> None:
        if len(self.moves) == len(self.map.map) - 1:
            self.moves.pop(0)
        self.moves.append((color, position, self.chips_count))

    def update_game(self, color: tuple, position: tuple) -> None:
        self.game_timer.reset_timer()
        self.current_player = (self.current_player + 1) % len(self.players)
        self.map.put_chip(color, position)
        self.chips_count += 1
        self.add_move_in_stat(color, position)
        self.map.reset_free_point_list(position)

    def prepare_game(self, players: list) -> None:
        self.reset_game()
        self.players = players

    def reset_game(self) -> None:
        self.game_timer.reset_timer()
        self.statistic.download_score_table()
        self.players.clear()
        self.map.map.clear()
        self.map.prepare_map()
        self.chips_count = 0
        self.current_player = 0
        self.moves.clear()

    @property
    def time_left(self) -> str:
        return str(self.game_timer)

    def update_game_pointer(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def get_statistic(self) -> dict:
        return self.statistic.high_score_table

    def get_current_player_color(self) -> tuple:
        return self.players[self.current_player].color
