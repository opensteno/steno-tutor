# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test ChordHolder operation--mostly that it can return canon words."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import os
import unittest

from fly.translation import wordstochords
from fly.utils import dictionaryreader
from fly.utils import files as fileutils


class ChordHolderTest(unittest.TestCase):

    """Return the canon word or acceptable alternatives from ChordHolder."""

    def setUp(self):

        """Read dummy categorization dict. Note: the categories are random."""
        
        data_dir = fileutils.get_test_data_directory()
        cat_dict_path = os.path.join(data_dir, "word_category.json")
        cat_dict = dictionaryreader.load_dict(cat_dict_path)
        self.cat_dict = cat_dict

    def test_get_canon_word(self):
        
        """Check canon word returned."""

        # Categories listed are what's in test data word_category.json
        chord_list = ["KR", # alternative
                      "AUL", # canon
                      "PARD", # unknown
                     ]

        chord_holder = wordstochords.ChordHolder(chord_list)
        expected_chord = "AUL"
        canon_chord = chord_holder.get_canon_chord(self.cat_dict)
        self.assertEquals(expected_chord, canon_chord)
        
    def test_get_alternative_word(self):
        
        """If there's no canon, return alternative."""

        # Categories listed are what's in test data word_category.json
        chord_list = ["KR", # alternative
                      "PARD", # unknown
                      "KHR", # misstroke
                     ]

        chord_holder = wordstochords.ChordHolder(chord_list)
        expected_chord = "KR"
        canon_chord = chord_holder.get_canon_chord(self.cat_dict)
        self.assertEquals(expected_chord, canon_chord)
    
    def test_get_unknown_word(self):
        
        """If there's no canon or alternative, return unknown."""

        # Categories listed are what's in test data word_category.json
        chord_list = ["PARD/O*PB", # misstroke
                      "PARD", # unknown
                      "KHR", # misstroke
                     ]

        chord_holder = wordstochords.ChordHolder(chord_list)
        expected_chord = "PARD"
        canon_chord = chord_holder.get_canon_chord(self.cat_dict)
        self.assertEquals(expected_chord, canon_chord)
    
    def test_get_brief_word(self):
        
        """If there's no canon, alternative, or unknown return brief."""

        # Categories listed are what's in test data word_category.json
        chord_list = ["PARD/O*PB", # misstroke
                      "SHRAOEP", # brief
                      "KHR", # misstroke
                     ]

        chord_holder = wordstochords.ChordHolder(chord_list)
        expected_chord = "SHRAOEP"
        canon_chord = chord_holder.get_canon_chord(self.cat_dict)
        self.assertEquals(expected_chord, canon_chord)
    
    def test_get_misstroke_word(self):
        
        """There are no options left! Return misstroke."""

        # Categories listed are what's in test data word_category.json
        chord_list = ["PARD/O*PB", # misstroke
                     ]

        chord_holder = wordstochords.ChordHolder(chord_list)
        expected_chord = "PARD/O*PB"
        canon_chord = chord_holder.get_canon_chord(self.cat_dict)
        self.assertEquals(expected_chord, canon_chord)

    def test_get_random(self):
        
        """No categorization for chords in chord list, return random."""

        # Categories listed are what's in test data word_category.json
        chord_list = ["BLAH", # not in dict
                      "HAHAHA", # not in dict
                     ]

        chord_holder = wordstochords.ChordHolder(chord_list)
        canon_chord = chord_holder.get_canon_chord(self.cat_dict)
        self.assertTrue(canon_chord in chord_list)


if __name__ == '__main__':
    unittest.main()


