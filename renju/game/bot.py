from renju.game import map, const, player
import random


class Bot(player.Player):
    @staticmethod
    def random() -> tuple:
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        return x, y

    def make_move(self, game_map: map.Map, bot_level: int):
        current_color_position = (0, (0, 0))
        another_color_position = (0, (0, 0))
        if len(game_map.free_point_list) == 0 or bot_level == 0:
            return self.random()
        for point in game_map.free_point_list:
            white_sizes = []
            for direction in const.directions:
                white_sizes.append(game_map.check_winner(point[0],
                                                         point[1],
                                                         direction,
                                                         (255, 255, 255),
                                                         1))
            if len(white_sizes) != 0:
                white_sizes.sort(reverse=True)
                if white_sizes[0] > current_color_position[0]:
                    current_color_position = (white_sizes[0], point)
            if current_color_position[0] >= 4\
                    and (255, 255, 255) != self.color:
                return point
            black_sizes = []
            for direction in const.directions:
                black_sizes.append(game_map.check_winner(point[0],
                                                         point[1],
                                                         direction,
                                                         (0, 0, 0),
                                                         1))
            if not game_map.check_game_rule((0, 0, 0), black_sizes):
                continue
            elif len(black_sizes) != 0:
                black_sizes.sort(reverse=True)
                if black_sizes[0] > another_color_position[0]:
                    another_color_position = (black_sizes[0], point)
            if another_color_position[0] >= 4 and (0, 0, 0) != self.color:
                return point
        return another_color_position[1] if self.color == (0, 0, 0) \
            else current_color_position[1]
