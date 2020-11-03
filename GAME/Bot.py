from GAME import Player
import random


class Bot(Player.Player):
    def make_move(self):
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        return x, y