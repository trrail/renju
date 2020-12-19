from renju.game.map import Map
from renju.game.color import Color


class Player:
    def __init__(self, current_color: tuple, callback):
        self.color = current_color
        self.colors = list(Color)
        # callback - это функция define_position в классе Window
        self.callback = callback

    def make_move(self, game_map: Map, players_and_bots_count: int) -> None:
        return self.callback()
