from renju.game import map, const, player
import random


class EasyModeBot(player.Player):
    @staticmethod
    def random() -> tuple:
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        return x, y

    def make_move(self, game_map: map.Map, bots_counts: int):
        return self.random()


class HardModeBot(EasyModeBot):
    def make_move(self, game_map: map.Map, bots_count: int) -> tuple:
        if len(game_map.free_point_list) == 0:
            return self.random()
        current_color_more_effective_position = \
            self.check_positions(self.color, game_map)

        another_players_positions = []
        for i in range(bots_count-1):
            another_player_color = self.change_color(self.color)
            another_players_positions.append(
                self.check_positions(another_player_color, game_map))
        for positions in another_players_positions:
            if current_color_more_effective_position[0] > positions[0]:
                return current_color_more_effective_position[1]
            if current_color_more_effective_position[0] < positions[0] \
                    and positions[0] >= 4:
                return positions[1]
        return current_color_more_effective_position[1]

    def change_color(self, color: tuple) -> tuple:
        return self.colors.next_to_current_color(color)

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
