import time

class Stopwatch():
    def __init__(self):
        self.start_time = time.time()
        self.last_time = self.start_time
        self.total_time = 0
        self.paused_time = 0
        self.time_rightnow = 0

    def reset_timer(self):
        self.last_time = time.time()

    def current_time(self):
        self.time_rightnow = round((time.time() - self.last_time), 2)
        return self.time_rightnow

    def total_time(self):
        return round((time.time() - self.total_time), 2)

    def pause_time(self):
        self.paused_time = self.time_rightnow

    def unpause_time(self):
        self.last_time = time.time() - self.paused_time
        self.paused_time = 0