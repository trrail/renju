import pytest
from renju.game.bot import Bot
from renju.game.map import Map


@pytest.fixture()
def bot():
    bot = Bot((255, 255, 255))
    return bot


def test_random(bot):
    x_bool = 0 <= bot.random()[0] <= 14
    y_bool = 0 <= bot.random()[1] <= 14
    assert x_bool is True
    assert y_bool is True


def test_hard_bot(bot):
    map = Map()
    map.prepare_map()
    for y in range(4):
        map.put_chip((0, 0, 0), (0, y))
        map.reset_free_point_list((0, y))
    assert bot.make_move(map, 1) == (0, 4)
