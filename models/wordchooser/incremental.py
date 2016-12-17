# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.import random

"""Add extra words to lesson as user improves."""

import random
import logging
logger = logging.getLogger(__name__)

from fly import config
from fly.models.wordchooser import interface


class RetrieveIntroduceIncrement(interface.WordChooserInterface):

    """
    Start with a minimum of words, and add extra words when the user meets 
    accuracy/speed requirements (see Fly/config.py for how to set the 
    requirements). Extra words are removed if the user doesn't meet 
    requirements, but the base words are always available.
    """

    BASE_WORD_NUMBER = config.BASE_WORD_NUMBER
    WORDS_BEFORE_WORD_ADDED = config.WORDS_BEFORE_WORD_ADDED

    def __init__(self, word_translation_dict, word_list):

        """
        @param word_translation_dict: dict mapping steno chord to 
                                      english translation for every
                                      chord in word_list
        @param word_list: list of steno words to present to user

        @type word_translation_dict: dict
        @type word_list: list
        """

        self.word_translation_dict = word_translation_dict
        self.word_list = word_list
        self.previous_translation = ""

        self.level = 1
        self.available_word_count = min(len(word_list), self.BASE_WORD_NUMBER) 
        self.base_words = word_list[0:self.available_word_count]
        self.extra_words = []
        
        # Get first word not in base_words
        self.new_word_index = self.available_word_count 
        self.counter = 0

    def get_word_and_translation(self, level):
        self.__adjust_extra_words(level)
        
        word, translation = self.__get_word_and_translation_from_list()
        i = 0
        while translation == self.previous_translation:
            word, translation = self.__get_word_and_translation_from_list()
            i += 1
            if i > 1000:
                break
        self.previous_translation = translation
        return word, translation

    def __get_word_and_translation_from_list(self):

        """Choose word+translation from base and extra list randomly.
        
        @return: tuple of (steno chord, translation) for user to type 
        @rtype: (str, str)
        """

        word = random.choice(self.base_words + self.extra_words)
        translation = self.word_translation_dict[word]

        return word, translation

    def __adjust_extra_words(self, level):

        """Add or remove extra words based on level.

        If level is increasing or staying steady, add words. Otherwise
        remove words. Don't remove base words.
        """

        if level > 1 and level >= self.level:
            if self.counter > self.WORDS_BEFORE_WORD_ADDED:
                # Maintained or exceeded level? Good. Add a new word.
                if self.new_word_index < len(self.word_list):
                    self.extra_words.append(self.word_list[self.new_word_index])
                    self.new_word_index += 1
                    self.counter = 0
                    logger.info("New word added: %s" \
                        % self.word_list[self.new_word_index])
            else:
                self.counter += 1
        else:
            # Dropped to a lower level? Remove word if possible.
            if self.extra_words:
                word_pop = self.extra_words.pop()
                self.new_word_index = max(self.available_word_count, 
                                          self.new_word_index - 1)
                logger.info("Word removed: %s" % word_pop)


