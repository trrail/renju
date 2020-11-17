from gui import chip


class Map:
    def __init__(self):
        self.map = []
        self.width = 15
        self.height = 15
        self.prepare_map()

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

    def check_winner(self, x: int, y: int, direction: tuple, color: tuple, length: int) -> int:
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

    @staticmethod
    def _increment_coordinates(length, x: int, y: int, direction: tuple) -> tuple:
        length += 1
        x += direction[0]
        y += direction[1]
        return length, x, y
