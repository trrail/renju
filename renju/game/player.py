from renju.game import map


class Player:
    def __init__(self, color: tuple):
        self.color = color

    def make_move(self, game_map: map.Map, bot_level: int) -> None:
        return None
