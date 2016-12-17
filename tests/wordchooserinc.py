# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Tests for word chooser incremental module."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from fly.models.wordchooser import incremental


class WordChooserIncrementalTest(unittest.TestCase):

    """Test that wordChooser incremental returns words incrementally."""

    def setUp(self):
        self.word_translation_dict = {'we': 'WE', 
                                     'of': '-F', 
                                     'acceptable': 'S*EBL', 
                                     'mission': 'PHEUGS', 
                                     'nun': 'TPH*UPB', 
                                     'midget': 'PHEUGT', 
                                     'haired': 'HAEURD', 
                                     'footprint': 'TPAOPBT', 
                                     'was': 'WA'}

        self.word_list = ["haired", "was", "we", "of", 
                          "nun", "mission", "acceptable"]

    def test_incremental_base(self):

        """Test incremental when level stays lowest. 

        Expect that only words up to BASE_WORD_NUMBER will be presented.
        """

        wc = incremental.RetrieveIntroduceIncrement(self.word_translation_dict,
                                                    self.word_list)
        level = 1
        first_word_list = self.word_list[:wc.BASE_WORD_NUMBER]
        for i in range(100):
            word, translation = wc.get_word_and_translation(level)
            self.assertTrue(word in first_word_list,
                            "actually word is %s, and list is "
                            "%s" % (word, first_word_list))
            self.assertTrue(self.word_translation_dict[word] == translation)

    def test_incremental_level_change(self):

        """Test incremental when level increases and decreases.

        Expect that words will be increased as level stays same at above min,
        and that when level drops, words will be removed.
        """

        wc = incremental.RetrieveIntroduceIncrement(self.word_translation_dict,
                                                    self.word_list)
        level = 2
        word_list = self.word_list[:wc.BASE_WORD_NUMBER]
        for i in range(wc.WORDS_BEFORE_WORD_ADDED * 2):
            word, translation = wc.get_word_and_translation(level)
            if i > wc.WORDS_BEFORE_WORD_ADDED:
                extra_words = ["mission", "acceptable"]
            else:
                extra_words = ["mission"]
            self.assertTrue(word in word_list + extra_words,
                            "actually word was %s and word list "
                           "%s for i %s" % (word, word_list + extra_words, i))
            self.assertTrue(self.word_translation_dict[word] == translation)
        
        extra_word_count = 0
        for i in range(30):
            level = 1
            word, translation = wc.get_word_and_translation(level)
            if word == "mission" or word == "acceptable":
                extra_word_count += 1
        self.assertTrue(extra_word_count <= 2)
    

if __name__ == '__main__':
    unittest.main()

