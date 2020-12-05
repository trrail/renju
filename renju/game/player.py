from renju.game.map import Map
from renju.game.color import Color


class Player:
    def __init__(self, current_color: tuple):
        self.color = current_color
        self.colors = Color()

    def make_move(self, game_map: Map, players_and_bots_count: int) -> None:
        return None
