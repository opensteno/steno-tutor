# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test of the lesson mapper."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fly.lessons import container
from fly.lessons.helpers.mapper import LessonWordChooserMapper
from fly.lessons.helpers.directive import DirectiveInterpreter
from fly.models.wordchooser import incremental, inorder, randomize

random = DirectiveInterpreter.RETRIEVAL_RANDOMIZE_DIRECTIVE
increment = DirectiveInterpreter.RETRIEVAL_INCREMENT_DIRECTIVE
in_order = DirectiveInterpreter.RETRIEVAL_IN_ORDER_DIRECTIVE

word_display = DirectiveInterpreter.DISPLAY_WORD_DIRECTIVE
sentence_display = DirectiveInterpreter.DISPLAY_SENTENCE_DIRECTIVE


class LessonMapperTest(unittest.TestCase):

    """Test mapping of Lesson to word chooser"""

    def setUp(self):
        
        """Create a mapper and lesson for the tests."""

        self.mapper = LessonWordChooserMapper()
        self.lesson = container.Lesson("test", "Test", "/some/path")

    def test_get_word_chooser_randomize(self):
        
        """Test randomize maps to RetrieveRandomize."""

        self.lesson.retrieval_directive = random
        self.lesson.display_directive = word_display
        word_chooser = self.mapper.get_word_chooser(self.lesson)
        self.assertTrue(type(word_chooser) == randomize.RetrieveRandomize)

    def test_get_word_chooser_randomize_sentence(self):
        
        """Test randomize maps to RetrieveRandomize in sentence mode"""

        self.lesson.retrieval_directive = random
        self.lesson.display_directive = sentence_display
        word_chooser = self.mapper.get_word_chooser(self.lesson)
        self.assertTrue(type(word_chooser) == randomize.RetrieveRandomize)

    def test_get_word_chooser_increment(self):
        
        """Test increment maps to RetrieveIntroduceIncrement."""

        self.lesson.retrieval_directive = increment
        self.lesson.display_directive = word_display
        word_chooser = self.mapper.get_word_chooser(self.lesson)
        self.assertTrue(type(word_chooser) == \
                        incremental.RetrieveIntroduceIncrement)
    
    def test_get_word_chooser_increment_sentence(self):
        
        """Increment maps to RetrieveIntroduceIncrement in sentence mode."""

        self.lesson.retrieval_directive = increment
        self.lesson.display_directive = sentence_display
        word_chooser = self.mapper.get_word_chooser(self.lesson)
        self.assertTrue(type(word_chooser) == \
                        incremental.RetrieveIntroduceIncrement)
        
    def test_get_word_chooser_inorder(self):
        
        """Test in_order maps to RetrieveInOrder."""

        self.lesson.retrieval_directive = in_order
        self.lesson.display_directive = word_display
        word_chooser = self.mapper.get_word_chooser(self.lesson)
        self.assertTrue(type(word_chooser) == \
                        inorder.RetrieveInOrder)
    
    def test_get_word_chooser_inorder_sentence(self):
        
        """Test in_order maps to RetrieveInOrderSentence in sentence mode."""

        self.lesson.retrieval_directive = in_order
        self.lesson.display_directive = sentence_display
        word_chooser = self.mapper.get_word_chooser(self.lesson)
        self.assertTrue(type(word_chooser) == \
                        inorder.RetrieveInOrderSentence)



if __name__ == '__main__':
    unittest.main()

