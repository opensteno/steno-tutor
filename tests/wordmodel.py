# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test the game model when running in word mode."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
from fly.models import gamemodel as game_model
from fly.models.wordchooser import leveldicts
from fly.models.inputinterpreter import word as input_word


class WordModelTest(unittest.TestCase):

    """Test GameModel when configured to run for word mode."""

    def setUp(self):

        """Create game model to test (configured for words)."""

        word_chooser = leveldicts.RetrieveFromLevelDictionaries()
        input_interpreter = input_word.InterpretForWord()
        self.model = game_model.GameModel("word", 
                                          word_chooser, 
                                          input_interpreter) 

    def test_get_qwerty_second_right(self):

        """A chord with an implicit right letter is handled correctly.
        
        For UD, the -D that would usually indicate the letter is on the 
        right hand side of the keyboard is missing. Since U is in the chord
        the right hand D is implied. Test that the model can handle this.
        """

        self.model.word = 'UD'
        self.model.translation = "you'd"

        qwerty_letters = self.model.get_qwerty_letters_to_type()
        expected_letters = ['M', '[']
        self.assertTrue(qwerty_letters == expected_letters)

    def test_get_qwerty(self):

        """Correct translation should be returned for input chord."""

        self.model.word = 'ST'
        self.model.translation = "it"

        qwerty_letters = self.model.get_qwerty_letters_to_type()
        expected_letters = ['QA', 'W']
        self.assertTrue(qwerty_letters == expected_letters)
    
    def test_get_qwerty_with_wildcard(self):

        """If a wildcard (*) appears, check it translates to qwerty.

        '*' should translate to TYGH as these are all '*' in steno.
        """

        self.model.word = 'SPHA*EURPL'
        self.model.translation = "antidisestablishmentarianism"

        qwerty_letters = self.model.get_qwerty_letters_to_type()
        expected_letters = ['QA', 'E', 'R', 'C', 'TYGH', 
                            'N', 'M', 'J', 'I', 'O']
        self.assertTrue(qwerty_letters == expected_letters)

    def test_get_qwerty_nitric(self):

        """For translation 'nitric' get qwerty letters"""

        self.model.word = 'TPHAOEUT/REUBG'
        self.model.translation = "nitric"

        qwerty_letters = self.model.get_qwerty_letters_to_type()
        expected_letters = ['W', 'E', 'R', 'C', 'V', 'N', 'M', 'P']
        self.assertTrue(qwerty_letters == expected_letters, 
                        "actually %s" % qwerty_letters)
  
    def test_all_chords_valid(self):

        """Any user-entered chord corresponding to correct is valid."""

        self.model.word = 'SKR'
        self.model.translation = 'have'

        self.model.input_word = 'SR'
        self.model.input_translation = 'have'
        self.assertTrue(self.model.right_word_entered() == True)


if __name__ == '__main__':
    unittest.main()


