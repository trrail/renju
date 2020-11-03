from GUI import Chip


class Map():
    def __init__(self):
        self.map = []
        self.width = 15
        self.height = 15
        self.prepare_map()

    def put_chip(self, color, position):
        self.map[position[0]][position[1]] = Chip.Chip(color, position)

    def prepare_map(self):
        for x in range(15):
            self.map.append([])
            for y in range(15):
                self.map[x].append(None)

    def get_condition(self, x, y):
        condition = x < 0 or \
                y < 0 or \
                y >= self.height or \
                x >= self.width
        return condition

    def check_winner(self, x, y, direction, color, length):
        dir_x_first = direction[0]
        dir_y_first = direction[1]
        dir_x_second = -direction[0]
        dir_y_second = -direction[1]
        inverse_dir = (-direction[0], -direction[1])
        while not self.get_condition(x + dir_x_first, y + dir_y_first) and \
                self.map[x + dir_x_first][y + dir_y_first] is not None \
                and self.map[x + dir_x_first][y + dir_y_first].color == color:
            length, dir_x_first, dir_y_first = self._increment_coordinates(
                length, dir_x_first, dir_y_first, direction)
        while not self.get_condition(x + dir_x_second, y + dir_y_second) and \
                self.map[x + dir_x_second][y + dir_y_second] is not None \
                and self.map[x + dir_x_second][y + dir_y_second].color == color:
            length, dir_x_second, dir_y_second = self._increment_coordinates(
                length, dir_x_second, dir_y_second, inverse_dir)
        return length

    @staticmethod
    def _increment_coordinates(length, x, y, direction):
        length += 1
        x += direction[0]
        y += direction[1]
        return length, x, y