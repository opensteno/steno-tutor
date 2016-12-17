# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test that utils.files calls all return valid file paths."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import os
import unittest

from fly.utils import files as fileutils


class FileUtilsTest(unittest.TestCase):

    """Every function in file utils should return a path that exists."""

    def test_get_base_directory(self):

        """Check the base dir exists and is a dir."""

        path = fileutils.get_base_directory()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))

    def test_get_dictionaries_directory(self):

        """Check the dictionary dir exists and is a dir."""

        path = fileutils.get_dictionaries_directory()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))
    
    def test_get_categorization_dict_path(self):

        """Check the categorization dict exists and is a file."""

        path = fileutils.get_categorization_dict_path()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isfile(path))

    def test_get_plover_dict_path(self):

        """Check the plover dict exists and is a file."""

        path = fileutils.get_plover_dict_path()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isfile(path))

    def test_get_level_dict_path(self):

        """Check all level dicts exist and are files."""

        for i in range(6):
            path = fileutils.get_level_dict_path(i + 1)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isfile(path))

    def test_get_lessons_directory(self):

        """Check the lessons dir exists and is a dir."""

        path = fileutils.get_lessons_directory()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))

    def test_get_test_data_directory(self):

        """Check the data dir exists and is a dir."""

        path = fileutils.get_test_data_directory()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))


if __name__ == '__main__':
    unittest.main()

