class Statistic:
    def __init__(self):
        self.high_score_table = {}
        self.download_score_table()

    def download_score_table(self) -> None:
        try:
            f = open('high_score_table.txt', 'r')
        except FileNotFoundError:
            f = open('high_score_table.txt', 'w')
            f.close()
        finally:
            f = open('high_score_table.txt', 'r')
            data = f.read().split('\n')
            if len(data) > 0:
                for string in data:
                    str = string.split('\t')
                    if len(str) == 2:
                        self.high_score_table.update({(str[0]): int(str[1])})
            f.close()
            print(self.high_score_table)

    def update_player(self, player_color: tuple) -> None:
        if not self.high_score_table.keys().__contains__(str(player_color)):
            self.high_score_table.update({str(player_color): 0})
        value = self.high_score_table.get(str(player_color))
        self.high_score_table.update({str(player_color): value + 1})
        print(self.high_score_table)
        self.write_in_file()

    def write_in_file(self):
        f = open('high_score_table.txt', 'w')
        f.truncate()
        for key in self.high_score_table.keys():
            f.write(key + '\t' + str(self.high_score_table.get(key)) + '\n')
        f.close()
