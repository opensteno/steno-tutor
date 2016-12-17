# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Random retrieval of words."""

import random

from fly.models.wordchooser import interface


class RetrieveRandomize(interface.WordChooserInterface):

    """Words are retrieved randomly from plover's dict."""

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
        self.previous_translation = ""
    
    def get_word_and_translation(self, level):
        word, translation = self.__get_word_and_translation_from_dict()
        i = 0
        while translation == self.previous_translation:
            word, translation = self.__get_word_and_translation_from_dict()
            i += 1
            if i > 1000:
                break
        self.previous_translation = translation
        return word, translation

    def __get_word_and_translation_from_dict(self):
        word = random.choice(self.word_translation_dict.keys())
        translation = self.word_translation_dict[word]
        return word, translation


