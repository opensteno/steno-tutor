# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Record typing speed of user."""

import time


class Timer(object):

    """For timing the typing speed of the user."""

    def __init__(self):
        self.reset()
        
    def reset(self):

        """Time starts now."""

        self.time_running = 0.001   # Never divide by 0
        self.start_time = time.time()

    def on_right_word_entered(self):

        """Record how long it took to enter a correct word."""

        self.end_time = time.time()
        self.time_running = self.end_time - self.start_time

    def get_time_running(self):

        """Return how long user took to enter correct word.

        @return: time to enter word
        @rtype: float
        """

        return self.time_running


