# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test the tint of the keys."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
from fly.gui.elements import keyboard


class KeyTintingTest(unittest.TestCase):

    """Test of the Tinter class.

    Tints key combinations to establish a connection between
    steno key combinations and english alphabet letters.
    """
    
    def test_tint_W(self):

        """Check qwerty W tints purple for T."""

        qwerty_letter_list = ['W']
        tint_map = keyboard.Tinter.get_tint_on_letters(qwerty_letter_list)
        expected_tint_map = {'W': keyboard.Tinter.TINT_MAP['T']}
        self.assertTrue(tint_map == expected_tint_map, 
                        "actually %s" % tint_map)

    def test_tint_S(self):

        """Check qwerty Q and A are recognised as S."""

        qwerty_letter_list = ['QA']
        tint_map = keyboard.Tinter.get_tint_on_letters(qwerty_letter_list)
        expected_tint_map = {'Q': keyboard.Tinter.TINT_MAP['S'],
                             'A': keyboard.Tinter.TINT_MAP['S']}
        self.assertTrue(tint_map == expected_tint_map, 
                        "actually %s" % tint_map)

    def test_tint_WSM(self):

        """Check qwerty W and S are recognised as D and M as U"""

        qwerty_letter_list = ['W', 'S', 'M']
        tint_map = keyboard.Tinter.get_tint_on_letters(qwerty_letter_list)
        expected_tint_map = {'W': keyboard.Tinter.TINT_MAP['D'],
                             'S': keyboard.Tinter.TINT_MAP['D'],
                             'M': keyboard.Tinter.TINT_MAP['U']}
        self.assertTrue(tint_map == expected_tint_map, 
                        "actually %s" % tint_map)
        
    def test_tint_KLsemicolon(self):

        """Check qwerty KL; are recognised as -X"""

        qwerty_letter_list = ['K', 'L', ';']
        tint_map = keyboard.Tinter.get_tint_on_letters(qwerty_letter_list)
        expected_tint_map = {'K': keyboard.Tinter.TINT_MAP['X'],
                             'L': keyboard.Tinter.TINT_MAP['X'],
                             ';': keyboard.Tinter.TINT_MAP['X']}
        self.assertTrue(tint_map == expected_tint_map, 
                        "actually %s" % tint_map)

    def test_tint_ASDF(self):

        """Check qwerty ASDF (in any order) are recognised as J"""

        qwerty_letter_list = ['S', 'D', 'F', 'QA']
        tint_map = keyboard.Tinter.get_tint_on_letters(qwerty_letter_list)
        expected_tint_map = {'A': keyboard.Tinter.TINT_MAP['J'],
                             'D': keyboard.Tinter.TINT_MAP['J'],
                             'Q': keyboard.Tinter.TINT_MAP['J'],
                             'F': keyboard.Tinter.TINT_MAP['J'],
                             'S': keyboard.Tinter.TINT_MAP['J']}
        self.assertTrue(tint_map == expected_tint_map, 
                        "actually %s" % tint_map)


if __name__ == '__main__':
    unittest.main()


