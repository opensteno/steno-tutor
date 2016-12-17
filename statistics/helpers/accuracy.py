# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Record the accuracy with which the user is entering words."""


class AccuracyMeter(object):

    """For recording how accurate user was in typing words."""

    def __init__(self):
        self.correct_word_count = 0
        self.total_word_count = 0

    def on_wrong_word_entered(self):

        """When wrong word is entered, record a word was completed."""

        self.total_word_count += 1

    def on_right_word_entered(self):

        """When right word is entered, record a correct word was completed."""

        self.correct_word_count += 1
        self.total_word_count += 1

    def get_word_count(self):

        """Get number of correct words entered.

        @return: how many correct words have been entered.
        @rtype: int
        """

        return self.correct_word_count

    def get_fraction_accurate(self):

        """Get number of words correct out of total number of words entered.

        @return: fraction of words correct out of words entered.
        @rtype: float
        """

        if self.total_word_count > 0:
            return float(self.correct_word_count)/float(self.total_word_count)
        return 0


