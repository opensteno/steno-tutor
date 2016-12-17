# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test the InterpretForWord input interpreter."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from fly.models.inputinterpreter import word as input_word


class WordInputInterpreterTest(unittest.TestCase):

    """Create a word inputInterpreter and test it."""

    def setUp(self):

        """Create word input interpreter."""

        self.input_interpreter = input_word.InterpretForWord()

    def test_get_input_for_single_chord(self):

        """Basic case of input word with no current input word.
        
        Expect input word and translation to return unchanged. 
        """

        input_word = "UL"
        input_translation = "you'll"
        word_to_type = "UL"
        current_input_word = ""
        
        results = self.input_interpreter.run(input_word, 
                                             word_to_type, 
                                             current_input_word, 
                                             input_translation)

        new_word = results[0]
        new_translation = results[1]
        self.assertTrue(new_word == input_word)
        self.assertTrue(new_translation == input_translation)

    def test_get_input_for_multichord(self):

        """Input word should be part of larger multichord word."""

        input_word = "TRA"
        input_translation = "{ultra^}"
        word_to_type = "UL/TRA/KOPB/S*EFRB/T*EUF" # ultraconservative
        current_input_word = "UL"
        
        results = self.input_interpreter.run(input_word, 
                                             word_to_type, 
                                             current_input_word, 
                                             input_translation)

        new_word = results[0]
        new_translation = results[1]
        self.assertTrue(new_word == "UL/TRA")
        self.assertTrue(new_translation == input_translation)

    def test_get_input_for_multichord_subchord(self):

        """Input word contains two chords, but is part of larger multichord.

        In this case, the larger multichord word should be recognised and 
        returned. 
        """

        input_word = "KOPB/S*EFRB"
        input_translation = "conserve"
        word_to_type = "UL/TRA/KOPB/S*EFRB/T*EUF" # ultraconservative
        current_input_word = "UL/TRA/KOPB"
        
        results = self.input_interpreter.run(input_word, 
                                             word_to_type, 
                                             current_input_word, 
                                             input_translation)

        new_word = results[0]
        new_translation = results[1]
        self.assertTrue(new_word == "UL/TRA/KOPB/S*EFRB", 
                        "actually %s" % new_word)
        self.assertTrue(new_translation == input_translation)


if __name__ == '__main__':
    unittest.main()

