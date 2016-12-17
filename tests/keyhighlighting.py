# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test the model can determine which keys to highlight."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
from fly.models import keyhighlighting


class KeyHighlightingTest(unittest.TestCase):

    """Test of the KeyHighlighter class.

    The keyhighlighter class is responsible for translating the 
    chord to type into qwerty keys that the user must press to generate
    the translation.
    """

    def setUp(self):
        self.klighter = keyhighlighting.KeyHighlighter()        
    
    def test_get_stroke_no_input(self):

        """Check the first stroke is returned when no user input."""

        stroke = self.klighter.get_stroke("AU/ROR/RA",
                                          "")
        self.assertTrue(stroke == "AU", "actually %s" % stroke)

    def test_get_stroke_first_stroke_typed(self):

        """Second stroke is returned when user enters first stroke."""

        stroke = self.klighter.get_stroke("AU/ROR/RA", 
                                          "AU")
        self.assertTrue(stroke == "ROR", "actually %s" % stroke)
    
    def test_get_stroke_first_stroke_typed_incorrectly(self):

        """First stroke returned when user enters first stroke incorrectly"""

        stroke = self.klighter.get_stroke("AU/ROR/RA", 
                                          "AI")
        self.assertTrue(stroke == "AU", "actually %s" % stroke)
    
    def test_get_stroke_second_stroke_typed(self):

        """Second stroke typed, so expect third stroke."""

        stroke = self.klighter.get_stroke("AU/ROR/RA", 
                                          "AU/ROR")
        self.assertTrue(stroke == "RA", "actually %s" % stroke)

    def test_get_stroke_single_stroke(self):

        """One chord only so return that."""

        stroke = self.klighter.get_stroke("AU", 
                                          "")
        self.assertTrue(stroke == "AU", "actually %s" % stroke)

    def test_get_stroke_single_stroke_done(self):

        """One chord only, user completed."""

        stroke = self.klighter.get_stroke("AU", 
                                          "AU")
        self.assertTrue(stroke == "AU", "actually %s" % stroke)
    
    def test_get_stroke_single_stroke_incorrect(self):

        """One chord only, user completed wrongly."""

        stroke = self.klighter.get_stroke("AU", 
                                          "XR")
        self.assertTrue(stroke == "AU", "actually %s" % stroke)
 
    def test_get_stroke_single_stroke_incomplete(self):

        """One chord only, user typed only part of it."""

        stroke = self.klighter.get_stroke("AU", 
                                          "A")
        self.assertTrue(stroke == "AU", "actually %s" % stroke)

    def test_get_real_letters_left_letters(self):

        """Letters on left are real, so return as they are."""

        word = "SR"
        real_letters = self.klighter.get_real_letters(word)
        
        self.assertTrue(real_letters == ["S", "R"])

    def test_get_real_letters_right_letters(self):

        """Work out all letters are on right even if only first is marked."""

        word = "-PBLG"
        real_letters = self.klighter.get_real_letters(word)
        
        self.assertTrue(real_letters == ["-P", "-B", "-L", "-G"])
    
    def test_get_real_letters_last_right(self):

        """Work out final letter must be on right."""

        word = "WHOF"
        real_letters = self.klighter.get_real_letters(word)
        
        self.assertTrue(real_letters == ["W", "H", "O", "-F"])

    def test_get_qwerty_letter_list(self):

        """Valid steno letters return qwerty equivalents."""

        real_letters = ["S", "-F"]

        qwerty_letters = self.klighter.get_qwerty_letter_list(real_letters)
        self.assertTrue(qwerty_letters == ["QA", "U"], 
                        "actually %s" % qwerty_letters)


if __name__ == '__main__':
    unittest.main()


