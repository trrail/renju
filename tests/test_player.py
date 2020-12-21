import pytest
from renju.game.player import Player
from renju.game.map import Map


def define_position() -> tuple:
    return 14, 3


@pytest.fixture()
def player():
    player = Player((0, 0, 0), callback=define_position)
    return player


def test_make_move(player):
    assert player.make_move(Map(), 1) == (14, 3)
