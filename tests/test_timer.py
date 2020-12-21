import pytest
from renju.game.timer import Timer
import time


@pytest.fixture()
def timer():
    return Timer()


def test_timer_to_string(timer):
    assert str(timer) == "2:00"
    time.sleep(3)
    timer.update_timer(None)
    assert str(timer) == "1:57"
