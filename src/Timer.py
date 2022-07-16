import datetime


class Timer:
    def __init__(self, game_len):
        self.start = datetime.datetime.now()
        self.finish = self.start + datetime.timedelta(minutes=game_len)
        self.game_len = game_len

    def __str__(self):
        ts = self.start.strftime("%H:%M:%S")
        tf = self.finish.strftime("%H:%M:%S")
        return f"Start time = {ts}, finish time = {tf}"

    def get_time_left(self):
        time_diff = self.finish - datetime.datetime.now()
        if time_diff > datetime.timedelta(0, 0, 0, 0, 0, 0, 0):
            return time_diff
        else:
            return datetime.timedelta(0, 0, 0, 0, 0, 0, 0)

    def restartTimer(self):
        self.start = datetime.datetime.now()
        self.finish = self.start + datetime.timedelta(minutes=self.game_len)

    def isPassed(self):
        if self.get_time_left().seconds == 0:
            return True
        else:
            return False
