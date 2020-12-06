import pytest
import os
from renju.game.game import Game
from renju.game.player import Player
from renju.game.bot import HardModeBot, EasyModeBot


@pytest.fixture()
def game():
    game = Game()
    return game


def test_prepare_game(game):
    game.prepare_game(2, 0, False)
    for player in game.players:
        assert type(player) is Player
    game.prepare_game(0, 2, True)
    for player in game.players:
        assert type(player) is HardModeBot
    game.prepare_game(1, 1, False)
    assert type(game.players[0]) is Player
    assert type(game.players[1]) is EasyModeBot
    os.remove("high_score_table.txt")


def test_update_game(game):
    game.prepare_game(2, 0, False)
    game.update_game((0, 0, 0), (2, 3))
    assert game.current_player == 1
    assert game.chips_count > 0
    assert len(game.moves) == 1
    os.remove("high_score_table.txt")


def test_add_move_in_stat(game):
    n = 0
    for i in range(15):
        game.add_move_in_stat((0, 0, 0), (n, i))
        n += 1
    assert game.moves[0][1] == (1, 1)
    os.remove("high_score_table.txt")


def test_make_move(game):
    game.prepare_game(2, 0, False)
    assert game.make_move((3, 0)) is None
    os.remove("high_score_table.txt")


def test_take_pos(game):
    game.prepare_game(1, 1, True)
    assert game.take_pos() is None
    game.update_game((0, 0, 0), (1, 1))
    assert game.take_pos() is not None
    os.remove("high_score_table.txt")


def test_reset_game(game):
    game.chips_count = 213
    game.current_player = 1
    game.add_move_in_stat((0, 0, 0), (1, 1))
    game.reset_game()
    assert game.chips_count == 0
    assert game.current_player == 0
    assert len(game.moves) == 0
    os.remove("high_score_table.txt")
