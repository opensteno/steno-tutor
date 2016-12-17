# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test the game model when running in alphabet mode."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from fly.data import alphabetdict as alphabet
from fly.models import gamemodel as game_model
from fly.models.wordchooser import randomize
from fly.models.inputinterpreter import alphabet as input_alphabet


class AlphabetModelTest(unittest.TestCase):

    """Test of the GameModel configured for alphabet mode."""

    def setUp(self):

        """Create game model to test (configured for alphabet)."""

        alphabet_word_list = [] # Dummy, not used
        word_chooser = randomize.RetrieveRandomize(alphabet.INVERSE_STENO, 
                                                   alphabet_word_list)
        input_interpreter = input_alphabet.InterpretForAlphabet()
        self.model = game_model.GameModel("alphabet", 
                                          word_chooser, 
                                          input_interpreter)

    def test_generate_word_and_translation(self):

        """Word generated should be in the steno alphabet."""

        self.model.generate_word_to_type()
        word, translation = self.model.get_display_word_and_translation()
        self.assertTrue(word in alphabet.STENO_ALPHABET.values())
        self.assertTrue(translation in alphabet.STENO_ALPHABET.keys())
        self.assertTrue(word == alphabet.STENO_ALPHABET[translation])

    def test_same_word_not_presented_consecutively(self):

        """The word to type should not be the same twice in a row.
        
        In Alphabet mode, the user should not be presented with the same 
        word to type twice consecutively, as it will appear to them as 
        if they have mistyped it.

        """
        previous_translation = ""

        for i in range(1000):
            self.model.generate_word_to_type()
            word, translation = self.model.get_display_word_and_translation()
            previous_translation = translation

    def test_wrong_word_entered(self):

        """User-entered incorrect word should be recognised as such."""

        self.model.word = 'SKWR'
        self.model.translation = 'J'

        self.model.input_word = 'LMN'
        self.model.input_translation = ''
        self.assertTrue(self.model.right_word_entered() == False)
        
    def test_right_word_entered(self):

        """User-entered correct word should be recognised as correct."""

        self.model.word = 'SKWR'
        self.model.translation = 'J'

        self.model.input_word = 'SKWR'
        self.model.input_translation = 'J'
        self.assertTrue(self.model.right_word_entered() == True)
       
    def test_get_qwerty_letters_to_type(self):

        """Test correct qwerty letters are returned for typing SKWR. 
        
        Since 'S' is one of the steno letters, and appears twice on the 
        qwerty keyboard, both letters corresponding to 'S' should be 
        returned, i.e. Q and A.
        """

        self.model.word = 'SKWR'
        self.model.translation = 'J'

        qwerty_letters = self.model.get_qwerty_letters_to_type()
        expected_letters = ['QA', 'S', 'D', 'F']
        self.assertTrue(qwerty_letters == expected_letters)

    def test_letters_given_key_on_right(self):

        """Model must distinguish between right-hand and left-hand letters."""

        self.model.word = '-T'
        self.model.translation = 'the'

        qwerty_letters = self.model.get_qwerty_letters_to_type()
        expected_letters = ['P']
        self.assertTrue(qwerty_letters == expected_letters)

    def test_alphabet_translation(self):

        """Translated letter should be translated as alphabet letter.

        When in alphabet mode, typing the wrong key should produce a
        translation of the alphabet key that the user pressed (for example, 
        if steno "S" is pressed, the translation should be "S" and not "is" --
        unless there's no alphabet translation (if it's an unknown chord). 
        """

        self.model.word = 'S'
        self.model.translation = 'S'
        self.model.set_input_word_and_translation("T", "blah")

        chord, translation = self.model.get_chord_and_translation()
        self.assertTrue(translation == "T", "actually %s" % translation)


if __name__ == '__main__':
    unittest.main()

