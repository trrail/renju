from renju.game import map, const, player
import random


class Bot(player.Player):
    @staticmethod
    def random() -> tuple:
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        return x, y

    def make_move(self, game_map: map.Map, bot_level: int):
        if len(game_map.free_point_list) == 0 or bot_level == 0:
            return self.random()
        current_color_more_effective_position = \
            self.check_positions(self.color, game_map)
        another_player_color = self.change_color(self.color)
        another_color_more_effective_position = \
            self.check_positions(another_player_color, game_map)
        if current_color_more_effective_position[0] >\
                another_color_more_effective_position[0]:
            return current_color_more_effective_position[1]
        if current_color_more_effective_position[0] <\
                another_color_more_effective_position[0] \
                and another_color_more_effective_position[0] >= 4:
            return another_color_more_effective_position[1]
        return current_color_more_effective_position[1]

    @staticmethod
    def change_color(color: tuple) -> tuple:
        return (255, 255, 255) if color == (0, 0, 0) else (0, 0, 0)

    @staticmethod
    def check_positions(color: tuple, game_map: map.Map) -> tuple:
        color_positions = (0, (0, 0))
        for point in game_map.free_point_list:
            all_length = []
            for direction in const.directions:
                all_length.append(game_map.check_winner(point[0],
                                                        point[1],
                                                        direction,
                                                        color,
                                                        1))
            if not game_map.check_game_rule(color, all_length):
                continue
            if len(all_length) != 0:
                all_length.sort(reverse=True)
                if all_length[0] > color_positions[0]:
                    color_positions = (all_length[0], point)
        return color_positions
