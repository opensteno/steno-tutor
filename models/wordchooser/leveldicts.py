# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Choose words from plover's dict, based on difficulty level."""

import random

from fly.models.wordchooser import interface
from fly.utils import dictionaryreader as dictread
from fly.utils import files as fileutils
from fly.translation import wordstochords


class RetrieveFromLevelDictionaries(interface.WordChooserInterface):

    """
    Six dictionaries have been generated (see data/generation/
    leveldictextraction.py) which have varying levels of difficulty in
    terms of number of keys to press simultaneously. The level the user
    is at, which depends on user's speed and accuracy, determines which
    dictionary the word to type is randomly drawn from.
    """

    dictionary_filename_1 = fileutils.get_level_dict_path(1)
    dictionary_filename_2 = fileutils.get_level_dict_path(2)
    dictionary_filename_3 = fileutils.get_level_dict_path(3)
    dictionary_filename_4 = fileutils.get_level_dict_path(4)
    dictionary_filename_5 = fileutils.get_level_dict_path(5)
    dictionary_filename_6 = fileutils.get_level_dict_path(6)
    word_category_filepath = fileutils.get_categorization_dict_path()

    def __init__(self):
        self.dictionary_1 = dictread.load_dict(self.dictionary_filename_1)
        self.dictionary_2 = dictread.load_dict(self.dictionary_filename_2)
        self.dictionary_3 = dictread.load_dict(self.dictionary_filename_3)
        self.dictionary_4 = dictread.load_dict(self.dictionary_filename_4)
        self.dictionary_5 = dictread.load_dict(self.dictionary_filename_5)
        self.dictionary_6 = dictread.load_dict(self.dictionary_filename_6)
        self.word_cat_dict = dictread.load_dict(self.word_category_filepath)

        self.previous_translation = ""

        # Start at lowest level
        self.dictionary = self.dictionary_1

    def get_word_and_translation(self, level):

        word = self.get_random_canon_word()
        translation = self.dictionary[word]
        return word, translation
    
    def get_random_canon_word(self):

        """Chord returned will be canon or uncategorized."""

        word = random.choice(self.dictionary.keys())
        if word in self.word_cat_dict and \
           self.word_cat_dict[word] != wordstochords.CANON:
            return self.get_random_canon_word()

        return word

    def set_level(self, level):
        self.dictionary = eval("self.dictionary_%s" % level)


