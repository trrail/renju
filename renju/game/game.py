from renju.game import map, statistic, const, bot, player
from renju.game.color import Color


class Game:
    def __init__(self):
        self.players = []
        self.map = map.Map()
        self.chips_count = 0
        self.current_player = 0
        self.moves = []
        self.winner_size = []
        self.statistic = statistic.Statistic()
        self.color = Color()
        self.timer = 12000

    def take_pos(self) -> tuple:
        # Вернёт:
        # - None, если Player
        # - Tuple, если Bot
        self.update_timer(make_move=False)
        return self.players[self.current_player].make_move(self.map, len(self.players))

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
            self.winner_size.append(self.map.check_winner(position[0],
                                                          position[1],
                                                          direction,
                                                          color,
                                                          1))
        self.winner_size.sort(reverse=True)
        if self.winner_size[0] == 5 and self.map.check_game_rule(color, self.winner_size):
            self.statistic.update_player(color)
            return color

    def add_move_in_stat(self, color: tuple, position: tuple) -> None:
        if len(self.moves) == 14:
            self.moves.pop(0)
        self.moves.append((color, position, self.chips_count))

    def update_game(self, color: tuple, position: tuple) -> None:
        self.current_player = (self.current_player + 1) % len(self.players)
        self.map.put_chip(color, position)
        self.chips_count += 1
        self.add_move_in_stat(color, position)
        self.map.reset_free_point_list(position)
        self.update_timer(make_move=True)

    def prepare_game(self, players_count: int, bot_counts: int, bot_level: int) -> None:
        self.reset_game()
        for gamer in range(players_count):
            self.players.append(player.Player(self.color.next_color(players_count + bot_counts)))
        for bot_player in range(bot_counts):
            self.players.append(bot.EasyModeBot(self.color.next_color(players_count + bot_counts)) if bot_level == 0
                                else bot.HardModeBot(self.color.next_color(players_count + bot_counts)))

    def reset_game(self) -> None:
        self.players.clear()
        self.map.map.clear()
        self.map.prepare_map()
        self.chips_count = 0
        self.current_player = 0
        self.moves.clear()
        self.color.reset()
        self.update_timer(make_move=True)

    def update_current_player_pointer(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def get_statistic(self) -> dict:
        return self.statistic.high_score_table

    def get_timer(self) -> str:
        minutes = self.timer // 6000
        seconds = (self.timer - minutes * 6000) // 100
        return str(int(minutes)) + ":" + str(int(seconds))

    def get_current_player_color(self) -> tuple:
        return self.players[self.current_player].color

    def update_timer(self, make_move: bool) -> None:
        if make_move:
            self.timer = 12000
        elif self.timer == 0:
            self.timer = 12000
            self.update_current_player_pointer()
        else:
            self.timer -= 0.5
