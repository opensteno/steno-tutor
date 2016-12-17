# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test of the dictionary reader util."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import os
import unittest

from fly.utils import dictionaryreader as dictreader 
from fly.utils import files as fileutils


class DictionaryReaderUtilsTest(unittest.TestCase):

    """The dictionary reader loads json dicts."""

    def test_load_dummy_dict(self):

        """Load a dict and ensure contents are as expected."""

        data_dir = fileutils.get_test_data_directory()
        dummy_dict_path = os.path.join(data_dir, "dummy_dict.json")
        self.assertTrue(os.path.exists(dummy_dict_path), 
                        "Missing data for test: %s!" % dummy_dict_path)

        d = dictreader.load_dict(dummy_dict_path)
        self.assertTrue(type(d) == dict)
        self.assertTrue(d["-F"] == "of")


if __name__ == '__main__':
    unittest.main()

