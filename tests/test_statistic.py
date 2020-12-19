import pytest
import os
from renju.game.statistic import Statistic


@pytest.fixture()
def statistic():
    statistic = Statistic()
    os.remove("high_score_table.txt")
    f = open("high_score_table.txt", "w")
    f.write("(0, 0, 0)\t3\n(255, 255, 255)\t2\n")
    f.close()
    statistic.download_score_table()
    return statistic


def test_download_score_table(statistic):
    assert statistic.high_score_table.get("(0, 0, 0)") == 3
    assert statistic.high_score_table.get("(255, 255, 255)") == 2
    os.remove("high_score_table.txt")


def test_update_player(statistic):
    statistic.update_player((0, 0, 0))
    assert statistic.high_score_table.get("(0, 0, 0)") == 4
    os.remove("high_score_table.txt")


def test_write_in_file(statistic):
    statistic.update_player((255, 255, 255))
    statistic.write_in_file()
    f = open("high_score_table.txt", "r")
    data = f.read()
    f.close()
    assert data == "(0, 0, 0)\t3\n(255, 255, 255)\t3\n"
