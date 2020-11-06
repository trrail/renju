from game import player
from game import bot
from game import map
from game import const


class Game:
    def __init__(self, is_bot: bool):
        self.players = [player.Player((0, 0, 0)),
                        bot.Bot((255, 255, 255)) if is_bot else player.Player((255, 255, 255))]
        self.map = map.Map()
        self.is_bot = is_bot
        self.chips_count = 0
        self.current_player = 0

    def take_pos(self):
        # Вернёт:
        # - None, если Player
        # - Tuple, если Bot
        return self.players[self.current_player].make_move()

    def make_move(self, position: tuple) -> tuple:
        if self.map.point_is_free(position):
            color = self.players[self.current_player].color
            self.current_player = (self.current_player + 1) % len(self.players)
            self.map.put_chip(color, position)
            self.chips_count += 1
            return self.check_winner(position, color)

    def check_winner(self, position: tuple, color: tuple):
        # Определяет, выйграл ли предыдущий
        for direction in const.directions:
            length = self.map.check_winner(position[0], position[1], direction, color, 1)
            if length >= 5:
                return color
