import pytest
from renju.game.player import Player
from renju.game.map import Map


@pytest.fixture()
def player():
    player = Player((0, 0, 0))
    return player


def test_make_move(player):
    assert player.make_move(Map(), 1) is None
