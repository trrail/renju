import pytest
from renju.game.bot import HardModeBot
from renju.game.map import Map


@pytest.fixture()
def bot():
    bot = HardModeBot((255, 255, 255))
    return bot


def test_random(bot):
    x_bool = 0 <= bot.random()[0] <= 14
    y_bool = 0 <= bot.random()[1] <= 14
    assert x_bool is True
    assert y_bool is True


def test_hard_bot(bot):
    game_map = Map()
    game_map.prepare_map()
    for y in range(1, 4):
        game_map.put_chip((0, 0, 0), (y, y))
        game_map.reset_free_point_list((y, y))
    assert bot.make_move(game_map, 2) == (0, 0)
