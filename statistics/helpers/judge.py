# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Judge whether a user should progress based on typing speed and accuracy."""

import logging
logger = logging.getLogger(__name__)

from fly import config


class LevellerJudge(object):

    """
    Uses information about accuracy and speed to determine
    whether a user should progress to the next level.
    """

    MIN_LEVEL = 1
    MAX_LEVEL = 6

    WORDS_DELTA_TO_LEVEL_UP = config.WORDS_DELTA_TO_LEVEL_UP
    ACCURACY_FRACTION_THRESHOLD = config.ACCURACY_FRACTION_THRESHOLD 
    SPEED_WORDS_PER_MIN_THRESHOLD = config.SPEED_WORDS_PER_MIN_THRESHOLD

    def __init__(self):
        self.previous_total_words = 0
        self.current_level = 1
        self.previous_level = 1

    def get_level(self, total_words, accuracy, speed):

        """Return level user is currently at.

        @param total_words: number of words typed during game.
        @param accuracy: number of words correct out of total number of 
                         words typed.
        @param speed: words per minute the user is typing.

        @type total_words: int
        @type accuracy: float
        @type speed: float
        """

        total_words_delta = total_words - self.previous_total_words 
        if total_words_delta > self.WORDS_DELTA_TO_LEVEL_UP:

            if accuracy > self.ACCURACY_FRACTION_THRESHOLD and \
               speed > self.SPEED_WORDS_PER_MIN_THRESHOLD:
                self.current_level += 1
                self.current_level = min(self.current_level, self.MAX_LEVEL)
                if self.current_level != self.previous_level:
                    logger.info("Level up: %s" % self.current_level)
            else:
                self.current_level -= 1
                self.current_level = max(self.current_level, self.MIN_LEVEL)
                if self.current_level != self.previous_level:
                    logger.info("Level down: %s" % self.current_level)

            self.previous_level = self.current_level
            self.previous_total_words = total_words

        return self.current_level


