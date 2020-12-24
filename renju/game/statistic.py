import pathlib
import json
from renju.game.color import Color


class Statistic:
    HIGH_SCORE_FILE_NAME = "HIGH_SCORE_TABLE.json"

    def __init__(self):
        self.statistic_file = pathlib.Path(self.HIGH_SCORE_FILE_NAME)
        self.high_score_table = {}

    def download_score_table(self) -> None:
        if not self.statistic_file.exists():
            self.write_in_file()
        with open(self.statistic_file, "r") as file:
            self.high_score_table = json.load(file)

    def update_player(self, player_color: tuple) -> None:
        if not Color.toRGB(player_color) in self.high_score_table.keys():
            self.high_score_table.update({Color.toRGB(player_color): 0})
        value = self.high_score_table.get(Color.toRGB(player_color))
        self.high_score_table.update({Color.toRGB(player_color): value + 1})
        self.write_in_file()

    def write_in_file(self):
        with open(self.statistic_file, "w") as file:
            json.dump(self.high_score_table, file)
