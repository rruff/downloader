import time

class ProgressBar:
    def __init__(self, total_size, decimal_places = 1, fill = '█', bar_len = 100):
        self.total_size = total_size
        self.places = decimal_places
        self.fill = fill
        self.bar_len = bar_len

    def update(self, progress):
        percent = self._percent_complete(progress)
        bar = self._bar(progress)
        print(f'\r| {bar} | {percent}%', end='\r')

        if progress == self.total_size:
            print()

    def _percent_complete(self, progress):
        """ Returns the percent complete as a formatted string. """
        return ("{0:." + str(self.places) + "f}").format(100 * (progress / float(self.total_size)))

    def _bar(self, progress):
        filled_len = int(self.bar_len * progress // self.total_size)
        return self.fill * filled_len + '-' * (self.bar_len - filled_len)
