# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test of reading lesson directives."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from fly.lessons.helpers.directive import DirectiveInterpreter


class DirectiveInterpreterTest(unittest.TestCase):

    """The directive interpreter is responsible for finding directives."""
    
    def test_valid_directives(self):
        
        """Test valid directives are set."""
    
        di = DirectiveInterpreter("  <in_order, word>  blah")
        self.assertTrue(di.get_retrieval_directive() == "in_order")
        self.assertTrue(di.get_display_directive() == "word")
        
        di = DirectiveInterpreter("  <randomize, sentence>  blah")
        self.assertTrue(di.get_retrieval_directive() == "randomize")
        self.assertTrue(di.get_display_directive() == "sentence",
                        "actually %s" % di.get_display_directive())
            
    def test_one_invalid_directive(self):
        
        """Test when one directive is invalid, default returned."""
    
        di = DirectiveInterpreter("  <in_order, blah>  blah")
        self.assertTrue(di.get_retrieval_directive() == "in_order")
        self.assertTrue(di.get_display_directive() == "word")

    def test_both_directives_invalid(self):
        
        """Test when both directives are invalid, defaults are returned."""
    
        di = DirectiveInterpreter("<whatever, blah>")
        self.assertTrue(di.get_retrieval_directive() == "in_order")
        self.assertTrue(di.get_display_directive() == "word")

    def test_no_directives_specified(self):
        
        """When no directives are specified, defaults should be set."""
    
        di = DirectiveInterpreter("This file contains no directives.")
        self.assertTrue(di.get_retrieval_directive() == "in_order")
        self.assertTrue(di.get_display_directive() == "word")


if __name__ == '__main__':
    unittest.main()

