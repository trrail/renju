from renju.game import map, const, player
import random
from renju.game.vector import Vector


class EasyModeBot(player.Player):
    @staticmethod
    def random(game_map: map.Map) -> tuple:
        x = random.randint(0, len(game_map.map))
        y = random.randint(0, len(game_map.map))
        return x, y

    def make_move(self, game_map: map.Map, bots_counts: int):
        return self.random(game_map)


class HardModeBot(EasyModeBot):
    def make_move(self, game_map: map.Map, bots_count: int) -> tuple:
        if len(game_map.free_point_list) == 0:
            return self.random(game_map)
        current_color_more_effective_position = self.check_positions(
            self.color, game_map
        )

        another_players_positions = []
        for i in range(bots_count - 1):
            another_player_color = self.colors[i].value
            another_players_positions.append(
                self.check_positions(another_player_color, game_map)
            )
        for positions in another_players_positions:
            if current_color_more_effective_position[0] > positions[0]:
                return current_color_more_effective_position[1]
            if (
                current_color_more_effective_position[0] < positions[0]
                and positions[0] >= 4
            ):
                return positions[1]
        return current_color_more_effective_position[1]

    @staticmethod
    def check_positions(bot_color: tuple, game_map: map.Map) -> tuple:
        color_positions = (0, (0, 0))
        for point in game_map.free_point_list:
            all_length = []
            for direction in const.directions:
                all_length.append(
                    game_map.check_winner(Vector((point[0], point[1])),
                                          Vector(direction), bot_color, 1)
                )
            if not game_map.check_game_rule(bot_color, all_length):
                continue
            if len(all_length) != 0:
                all_length.sort(reverse=True)
                if all_length[0] > color_positions[0]:
                    color_positions = (all_length[0], point)
        return color_positions
