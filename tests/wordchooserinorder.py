# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test of retrieving words in order from lesson file."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import os
import unittest

from fly.models.wordchooser import inorder

from fly.lessons import container
from fly.lessons.helpers.filler import LessonFiller
from fly.utils import files as fileutils


def setUpTestLesson():

    """Make lesson object from test lesson in data dir."""

    test_data_dir = fileutils.get_test_data_directory()
    lesson_path = os.path.join(test_data_dir, "test.les")
    chords_path = os.path.join(test_data_dir, "test.chd")
    lesson_obj = container.Lesson("test", "Test", lesson_path)
    lesson_obj.chords_file_path = chords_path
    return lesson_obj


def setUpBigLesson():

    """Used by some test cases. A long first sentence is needed."""

    lesson = container.Lesson("test", "Test", "dummy/filepath.les")
    lesson.sentences_list = ['One Two Three Four Five', 'Six Seven Eight']
    lesson.chord_sentences_list = ['WUB TWO THRE TPOUR TPEUF', 
                                   'SEUBGS SEFPB AET']
    lesson.chords_list = ['WUB', 'TWO', 'THRE', 'TPOUR', 'TPEUF', 'SEUBGS',
                          'SEFPB', 'AET']
    lesson.translation_list = ['one', 'two', 'three', 'four', 'five', 
                               'six', 'seven', 'eight']
    lesson.sentence_map = {0: [0, 1, 2, 3, 4], 1: [5, 6, 7]}
    lesson.chord_translation_dict = {'TPEUF': 'five', 'TPOUR': 'four', 
                              'THRE': 'three', 'TWO': 'two', 
                              'WUB': 'one', 'SEUBGS': 'six', 
                              'SEFPB': 'seven', 'AET': 'eight'}
    return lesson


class RetrieveInOrderTest(unittest.TestCase):

    """Using an inorder word chooser, retrieve words in order."""

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

    def test_inorder(self):
        
        """Test words are retrieved in order."""

        wc = inorder.RetrieveInOrder(self.word_translation_dict, 
                                     self.word_list)

        index = 0
        for i in range(100):
            word, translation = wc.get_word_and_translation("dummy arg")
            if index >= len(self.word_list):
                index = 0
            self.assertTrue(word == self.word_list[index])
            self.assertTrue(self.word_translation_dict[word] == translation)
            index += 1

    def test_inorder_sentence(self):
        
        """Test sentence from which word in drawn can be retrieved."""
        
        lesson = setUpTestLesson()
        lessonFiller = LessonFiller()
        lessonFiller.populate_lesson(lesson)
        lesson.display_directive = "sentence"
        wc = inorder.RetrieveInOrderSentence(lesson)
       
        word, translation = wc.get_word_and_translation("no level")
        results = wc.get_display_word_and_translation("no level")
        self.assertTrue(len(results) == 2, 
                        "Wrong behaviour--expected overridden display")
        
        display_word = results[0] 
        display_translation = results[1]

        self.assertTrue(display_word == "WUB TWO THRE")
        self.assertTrue(display_translation == "One Two Three")

    def test_inorder_sentence_input_good(self):

        """Test input can be displayed sentence style.

        If the word chooser has returned a sentence to type, the input
        should match this, in that every word the user types in the sentence
        should appear and stay until the end of the sentence.
        """

        lesson = setUpBigLesson()       

        wc = inorder.RetrieveInOrderSentence(lesson)

        # Words are in order. Pretend the game is running, and the user is 
        # entering words, the first three.
        for i in range(3):
            results = wc.get_word_and_translation("no level")
            results_display = wc.get_display_word_and_translation("no level")

        self.assertTrue(results == ('THRE', 'three'))
        
        input_word, input_translation = wc.return_inputs('THRE', 'three')

        self.assertTrue(input_word == 'WUB TWO THRE',
                        "actually %s" % input_word)

        self.assertTrue(input_translation.lower() == "one two three",
                        "actually %s" % input_translation)

    def test_inorder_sentence_input_bad(self):

        """Test input can be displayed sentence style.

        If the word chooser has returned a sentence to type, the input
        should match this, in that every word the user types in the sentence
        should appear and stay until the end of the sentence.
        """

        lesson = setUpBigLesson()       

        wc = inorder.RetrieveInOrderSentence(lesson)

        # Words are in order. Pretend the game is running, and the user is 
        # entering words, the first three.
        for i in range(3):
            results = wc.get_word_and_translation("no level")
            results_display = wc.get_display_word_and_translation("no level")

        self.assertTrue(results == ('THRE', 'three'))
        
        input_word, input_translation = wc.return_inputs('SO', 'so')

        self.assertTrue(input_word == 'WUB TWO SO',
                        "actually %s" % input_word)

        self.assertTrue(input_translation.lower() == "one two so",
                        "actually %s" % input_translation)



if __name__ == '__main__':
    unittest.main()


