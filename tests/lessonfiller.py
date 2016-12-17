# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test the lesson filler class populates lesson correctly."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import os
import unittest

from fly.lessons.helpers.filler import LessonFiller
from fly.lessons import container
from fly.utils import files as fileutils


def setUpTestLesson():

    """Make lesson object from test lesson in data dir."""

    test_data_dir = fileutils.get_test_data_directory()
    lesson_path = os.path.join(test_data_dir, "test.les")
    chords_path = os.path.join(test_data_dir, "test.chd")
    lesson_obj = container.Lesson("test", "Test", lesson_path)
    lesson_obj.chords_file_path = chords_path
    return lesson_obj


class LessonFillerTest(unittest.TestCase):

    """The lesson filler reads the contents of lesson and translation files.

    It generates lists and maps that can be used by word choosers to present
    the words, and stores these on the lesson.
    """
    
    def test_get_chords_list(self):

        """Test that method returns a list of chords from a chords file."""
        
        lesson_obj = setUpTestLesson()
        chords_list = LessonFiller.get_chords_list(lesson_obj)

        self.assertTrue(chords_list == ["WUB", "TWO", "THRE", 
                                        "TPOUR", "TPEUF", "SEUBGS"],
                        "actually %s" % chords_list)

    def test_get_sentences_list(self):

        """Test that method returns a list of sentences from file."""
    
        lesson_obj = setUpTestLesson()
        sentence_list = LessonFiller.get_sentences_list(lesson_obj.file_path)

        self.assertTrue(sentence_list == ["One Two Three", 
                                          "Four Five Six"],
                        "actually %s" % sentence_list)
    
    def test_generate_translation_for_sentences(self):
        
        """Test that generating translation for sentences works."""
        
        sentences = ["For transient sorrows, simple wiles,",
                     "Praise, blame, love, kisses, tears, and smiles."]

        lessonFiller = LessonFiller()
        chords_list = []
        translation, sentence_map = \
                lessonFiller.generate_translation_for_sentences(sentences)

        expected_translation = ['for', 'transient', 'sorrows', ',', 'simple', 
                                'wiles', ',', 'praise', ',', 'blame', ',', 
                                'love', ',', 'kisses', ',', 'tears', ',', 
                                'and', 'smiles', '.'] 

        expected_sentence_map = {0: [0, 1, 2, 3, 4, 5, 6], 
                                 1: [7, 8, 9, 10, 11, 12, 13, 14, 
                                     15, 16, 17, 18, 19]}

        self.assertTrue(translation == expected_translation,
                        "actually %s" % translation)
        self.assertTrue(sentence_map == expected_sentence_map,
                        "actually %s" % sentence_map)

    def test_generate_word_indices(self):
        
        """Test generation of a list of the indices of words in a sentence.

        This is for the sentence map, so that there's a correspondence
        between words in a list and a list of sentences.
        For example, for sentences ["graceful and green", "as a stem"]
        words are ["graceful", "and", "green", "as", "a", "stem"]
        and the word indices we'd expect for sentence "as a stem"
        are [3,4,5] as those are the indices of the words in the word list.
        """

        # len["as a stem"]
        word_count = 3 
        # len["graceful", "and", "green", "as", "a", "stem"]
        total_word_count = 6 
        word_indices = LessonFiller.generate_word_indices(3, 6)
        self.assertTrue(word_indices == [3,4,5], "actually %s" % word_indices)

    def test_get_translation_dict(self):

        """Test get_translation_dict can return a dict of chord:translation."""

        lesson_obj = setUpTestLesson()

        lesson_obj.chords_list = ["WUB", "TWO", "THRE", 
                                  "TPOUR", "TPEUF", "SEUBGS"]

        lesson_obj.translation_list = ["One", "Two", "Three", 
                                       "Four", "Five", "Six"]

        translation_dict = LessonFiller.get_translation_dict(lesson_obj)

        expected_dict = {'TPEUF': 'Five', 'TPOUR': 'Four', 'THRE': 'Three', 
                         'TWO': 'Two', 'WUB': 'One', 'SEUBGS': 'Six'}

        self.assertTrue(translation_dict == expected_dict,
                        "actually %s" % translation_dict)

    def test_populate_lesson(self):
        
        """Test a lesson is populated from lesson and chord file contents."""
        
        lesson_obj = setUpTestLesson()
        lessonFiller = LessonFiller()
        lessonFiller.populate_lesson(lesson_obj)
 
        expected_sentences_list = ['One Two Three', 
                                   'Four Five Six']

        expected_chord_sentences_list = ['WUB TWO THRE',
                                         'TPOUR TPEUF SEUBGS']

        expected_chords_list = ['WUB', 'TWO', 'THRE',
                                'TPOUR', 'TPEUF', 'SEUBGS']

        expected_translation_list = ['one', 'two', 'three', 
                                    'four', 'five', 'six']

        expected_sentence_map = {0: [0, 1, 2], 1: [3, 4, 5]}

        expected_chord_translation_dict = {'TPEUF': 'Five', 'TPOUR': 'Four', 
                                           'THRE': 'Three', 'TWO': 'Two', 
                                           'WUB': 'One', 'SEUBGS': 'Six'}

        self.assertEquals(lesson_obj.sentences_list, expected_sentences_list)

        self.assertEquals(lesson_obj.chord_sentences_list, 
                          expected_chord_sentences_list)

        self.assertEquals(lesson_obj.chords_list, expected_chords_list)

        self.assertEquals(lesson_obj.translation_list, 
                          expected_translation_list)

        self.assertEquals(lesson_obj.sentence_map, expected_sentence_map)

        self.assertEquals(lesson_obj.chord_translation_dict,
                          expected_chord_translation_dict)


if __name__ == '__main__':
    unittest.main()

