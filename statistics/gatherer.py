# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Gathers statistics about user performance, such as speed and accuracy."""

from fly.statistics.helpers.timer import Timer
from fly.statistics.helpers.accuracy import AccuracyMeter
from fly.statistics.helpers.judge import LevellerJudge


class StatisticGatherer(object):

    """Provides stats, and uses stats to judge whether use should progress."""

    def __init__(self):
        self.timer = Timer()
        self.accuracy_meter = AccuracyMeter()
        self.level_judge = LevellerJudge()

    def on_right_word_entered(self):

        """Record that correct word has been entered."""

        self.timer.on_right_word_entered()
        self.accuracy_meter.on_right_word_entered()

    def on_wrong_word_entered(self):

        """Record that incorrect word has been entered."""

        self.accuracy_meter.on_wrong_word_entered()

    def get_words_per_min(self):

        """Returns typing speed in words per minute.
        
        @rtype: float
        """

        word_count = self.accuracy_meter.get_word_count()
        time_running = self.timer.get_time_running()
        seconds_per_minute = 60.0
        return seconds_per_minute * float(word_count/time_running)

    def get_fraction_accurate(self):

        """Get user accuracy as a number between 0 and 1.

        @rtype: float
        """

        return self.accuracy_meter.get_fraction_accurate()

    def get_level(self):

        """Judge user on speed and accuracy to determine their level.
        
        @return: level user is on. 
        @rtype: int
        """

        total_words = self.accuracy_meter.get_word_count()
        speed = self.get_words_per_min()
        accuracy = self.get_fraction_accurate()
        return self.level_judge.get_level(total_words, accuracy, speed)


