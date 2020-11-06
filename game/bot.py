from game import player
import random


class Bot(player.Player):
    def make_move(self) -> tuple:
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        return x, y
