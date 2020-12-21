import pytest
from renju.game.map import Map
from renju.game.const import directions
from renju.game.vector import Vector
from renju.game.chip import Chip


@pytest.fixture()
def board():
    board = Map()
    board.prepare_map()
    return board


def test_prepare_map(board):
    for x in range(15):
        for y in range(15):
            assert board.map[x][y] is None


def test_put_chip(board):
    board.put_chip((255, 255, 255), (0, 1))
    assert board.map[0][1] is not None


def test_get_condition(board):
    assert board.get_condition(Vector((-1, 1))) is True
    assert board.get_condition(Vector((12, 4))) is False
    assert board.get_condition(Vector((15, 0))) is True


def test_check_winner(board):
    for i in range(5):
        board.put_chip((255, 255, 255), (1, i))
    length = []
    for direction in directions:
        length.append(board.check_winner(Vector((1, 4)), Vector(direction), (255, 255, 255), 1))
    length.sort(reverse=True)
    assert length[0] == 5


def test_check_winner_diagonal(board):
    n = 0
    for i in range(5):
        board.put_chip((255, 255, 255), (n, i))
        n += 1
    length = []
    for direction in directions:
        length.append(board.check_winner(Vector((n - 1, 4)), Vector(direction),
                                         (255, 255, 255), 1))
    length.sort(reverse=True)
    assert length[0] == 5


def test_point_is_free(board):
    board.put_chip((0, 0, 0), (0, 0))
    assert board.point_is_free((0, 0)) is False
    assert board.point_is_free((0, 1)) is True


def test_reset_free_point_list(board):
    board.put_chip((0, 0, 0), (3, 3))
    board.reset_free_point_list((3, 3))
    board.put_chip((0, 0, 0), (3, 4))
    board.reset_free_point_list((3, 4))
    assert len(board.free_point_list) == 10


def test_check_game_rule(board):
    assert board.check_game_rule((0, 0, 0), [4, 4]) is False
    assert board.check_game_rule((0, 0, 0), [4, 5]) is False
    assert board.check_game_rule((255, 255, 255), [4, 4]) is True
    assert board.check_game_rule((0, 0, 0), [3, 3]) is True
