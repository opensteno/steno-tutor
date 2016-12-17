# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""This module manages finding and naming lessons."""

import os

from fly.lessons import container


class LessonFinder(object):

    """Assists in finding lessons."""

    LESSON_FILE_EXTENSION = '.les'

    def __init__(self, lessons_dir):

        """Init with lessons dir for easy testing.

        @param lessons_dir: file path for lessons directory
        @type lessons_dir: str
        """

        self.lessons_dir = lessons_dir
        self.lesson_file_name_list = []

    def find_lessons(self):

        """Look in the directory lessons and return lesson objects.

        @return: list of lesson objects corresponding to lessons in lesson dir.
        @rtype: list of L{Lesson}
        """

        lesson_list = []
        file_names = self.get_file_list()

        for name in file_names:
            raw_name, extension = os.path.splitext(name)

            # Create lesson object to represent lesson
            lesson_file_path = os.path.join(self.lessons_dir, name)
            lesson = container.Lesson(raw_name, self.get_nice_name(raw_name), 
                                      lesson_file_path)

            lesson_list.append(lesson) 

        return lesson_list

    def get_file_list(self):

        """Return a list of the lesson files in lesson dir."""

        if not self.lesson_file_name_list:
            file_names = os.listdir(self.lessons_dir)
            for name in file_names:
                raw_name, extension = os.path.splitext(name)
                if not extension == self.LESSON_FILE_EXTENSION:
                    continue
                self.lesson_file_name_list.append(name)

        return self.lesson_file_name_list

    @staticmethod
    def get_nice_name(lesson_name):
        
        """Convert lesson name 'example_one' to 'Example One'
        
        @return: prettified lesson name
        @rtype: str
        """
        
        lesson_name_words = lesson_name.split("_")
        lesson_name_caps_list = [n.capitalize() for n in lesson_name_words]
        return " ".join(lesson_name_caps_list)


