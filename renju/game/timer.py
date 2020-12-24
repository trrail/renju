import time


class Timer:
    DELAY = 120

    def __init__(self):
        self.start_time = time.perf_counter()
        self.time_left = self.DELAY

    def update_timer(self, event) -> None:
        current_time = time.perf_counter()
        changed_time = int(current_time - self.start_time)
        if changed_time >= self.DELAY:
            self.reset_timer()
            event()
        else:
            self.time_left = self.DELAY - changed_time

    def reset_timer(self):
        self.start_time = time.perf_counter()
        self.time_left = self.DELAY

    def __str__(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes}:{seconds if seconds > 9 else '0' + str(seconds)}"
