from renju.gui import chip
from renju.game import const


class Map:
    def __init__(self):
        self.map = []
        self.width = 15
        self.height = 15
        self.prepare_map()
        self.free_point_list = []

    def put_chip(self, color: tuple, position: tuple) -> None:
        # Добавляет новую фишку
        self.map[position[0]][position[1]] = chip.Chip(color, position)

    def prepare_map(self) -> None:
        for x in range(15):
            self.map.append([])
            for y in range(15):
                self.map[x].append(None)

    def get_condition(self, x: int, y: int) -> bool:
        condition = x < 0 or \
                    y < 0 or \
                    y >= self.height or \
                    x >= self.width
        return condition

    def check_winner(self, x: int, y: int,
                     direction: tuple,
                     color: tuple, length: int) -> int:
        x1_dir = direction[0]
        y1_dir = direction[1]
        x2_dir = -direction[0]
        y2_dir = -direction[1]
        inverse_dir = (-direction[0], -direction[1])
        while not self.get_condition(x + x1_dir, y + y1_dir) and \
                self.map[x + x1_dir][y + y1_dir] is not None and \
                self.map[x + x1_dir][y + y1_dir].color == color:
            length, x1_dir, y1_dir = self._increment_coordinates(
                length, x1_dir, y1_dir, direction)
        while not self.get_condition(x + x2_dir, y + y2_dir) and \
                self.map[x + x2_dir][y + y2_dir] is not None and \
                self.map[x + x2_dir][y + y2_dir].color == color:
            length, x2_dir, y2_dir = self._increment_coordinates(
                length, x2_dir, y2_dir, inverse_dir)
        return length

    def point_is_free(self, position: tuple) -> bool:
        if self.map[position[0]][position[1]] is None:
            return True
        return False

    def reset_free_point_list(self, position):
        for direction in const.point_around_directions:
            x_dir = position[0] + direction[0]
            y_dir = position[1] + direction[1]
            if 0 <= x_dir <= 14 \
                    and 0 <= y_dir <= 14 \
                    and self.map[x_dir][y_dir] is None:
                self.delete_point_from_list((x_dir, y_dir))
                self.free_point_list.append((x_dir, y_dir))
        self.delete_point_from_list(position)

    def delete_point_from_list(self, point: tuple):
        try:
            self.free_point_list.remove(point)
        except ValueError:
            pass

    @staticmethod
    def _increment_coordinates(length, x: int, y: int,
                               direction: tuple) -> tuple:
        length += 1
        x += direction[0]
        y += direction[1]
        return length, x, y

    @staticmethod
    def check_game_rule(color: tuple, winner_size: list) -> bool:
        if color == (0, 0, 0):
            if winner_size[0] > 5:
                return False
            if winner_size[0] > 3 and winner_size[1] > 3:
                return False
        return True
