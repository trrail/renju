import pathlib


class Statistic:
    HIGH_SCORE_FILE_NAME = "HIGH_SCORE_TABLE.txt"

    def __init__(self):
        self.statistic_file = pathlib.Path(self.HIGH_SCORE_FILE_NAME)
        self.high_score_table = {}

    def download_score_table(self) -> None:
        if not self.statistic_file.exists():
            self.statistic_file.touch()
        with open(self.statistic_file, "r") as file:
            data = file.read().split("\n")
            if len(data) > 0:
                for string in data:
                    stat = string.split("\t")
                    if len(stat) == 2:
                        self.high_score_table.update({(stat[0]): int(stat[1])})

    def update_player(self, player_color: tuple) -> None:
        if not self.high_score_table.keys().__contains__(str(player_color)):
            self.high_score_table.update({str(player_color): 0})
        value = self.high_score_table.get(str(player_color))
        self.high_score_table.update({str(player_color): value + 1})
        self.write_in_file()

    def write_in_file(self):
        with open(self.statistic_file, "w") as file:
            file.truncate()
            for key in self.high_score_table.keys():
                file.write(key + "\t" +
                           str(self.high_score_table.get(key)) + "\n")
