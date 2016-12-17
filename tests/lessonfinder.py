# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test of the lesson finder."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from fly.utils import files as fileutils
from fly.lessons import container
from fly.lessons.helpers.finder import LessonFinder


class LessonFinderTest(unittest.TestCase):

    """Lesson finder retrieves lesson files from directory."""

    def test_lesson_finder(self):
        
        """Search the test data directory for lessons."""

        test_dir = fileutils.get_test_data_directory()
        lessonFinder = LessonFinder(test_dir)

        lesson_list = lessonFinder.find_lessons()
        self.assertTrue(len(lesson_list) == 2)
        self.assertTrue(type(lesson_list[0]) == container.Lesson)

    def test_get_nice_name(self):

        """Test getting the nice name of a lesson."""

        lesson_name = LessonFinder.get_nice_name("howdy")
        self.assertTrue(lesson_name == "Howdy", "actually %s" % lesson_name)

        lesson_name = LessonFinder.get_nice_name("ADFSKJL")
        self.assertTrue(lesson_name == "Adfskjl", "actually %s" % lesson_name)

        lesson_name = LessonFinder.get_nice_name("read_it_twice")
        self.assertTrue(lesson_name == "Read It Twice", 
                        "actually %s" % lesson_name)

        lesson_name = LessonFinder.get_nice_name("bookAmazing")
        self.assertTrue(lesson_name == "Bookamazing",
                        "actually %s" % lesson_name)


if __name__ == '__main__':
    unittest.main()

