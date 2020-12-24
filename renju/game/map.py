from renju.game import const, chip
from renju.game.vector import Vector


class Map:
    MAP_SIZE = (15, 15)

    def __init__(self):
        self.map = []
        self.width = self.MAP_SIZE[0]
        self.height = self.MAP_SIZE[1]
        self.prepare_map()
        self.free_point_list = []

    '''
        Подготовка класса Map
    '''
    def prepare_map(self) -> None:
        for x in range(15):
            self.map.append([])
            for y in range(15):
                self.map[x].append(None)

    '''
        Поставить фишку на карту
    '''
    def put_chip(self, color: tuple, position: tuple) -> None:
        # Добавляет новую фишку
        self.map[position[0]][position[1]] = chip.Chip(color)

    def point_is_free(self, position: tuple) -> bool:
        if self.map[position[0]][position[1]] is None:
            return True
        return False
    '''
        Определение выйграшных позиций.
        Возвращают длину максимальной комбинации
        для выбранной точки выбранного цвета.
    '''
    def get_condition(self, vector: Vector) -> bool:
        condition = vector.x < 0 \
                    or vector.y < 0 \
                    or vector.y >= self.height \
                    or vector.x >= self.width
        return condition

    def check_winner(self, vector: Vector,
                     direction: Vector,
                     color: tuple,
                     length: int) -> int:
        first_dir = direction
        second_dir = -direction
        while not self.get_condition(vector + first_dir) \
                and self.get_point_from_vector(vector + first_dir) == color:
            length, first_dir = \
                self._increment_coordinates(length, first_dir, direction)
        while not self.get_condition(vector + second_dir) \
                and self.get_point_from_vector(vector + second_dir) == color:
            length, second_dir = \
                self._increment_coordinates(length, second_dir, -direction)
        return length

    def get_point_from_vector(self, vector: Vector):
        return self.map[vector.x][vector.y]

    @staticmethod
    def _increment_coordinates(length, vector: Vector,
                               direction: Vector) -> tuple:
        return length + 1, vector + direction

    '''
        Обрабатывается список свободных полей вокруг уже занятых.
        Данные методы нужны для HardModeBot
    '''
    def reset_free_point_list(self, position: tuple):
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

    '''
        Проверка соблюдения правил игры при ходе игрока
    '''
    @staticmethod
    def check_game_rule(color: tuple, winner_size: list) -> bool:
        if color == (0, 0, 0):
            if winner_size[0] > 5:
                return False
            if winner_size[0] > 3 and winner_size[1] > 3:
                return False
        return True
