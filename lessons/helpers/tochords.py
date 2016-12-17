# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Translate lesson file (plain text english) to steno chords file."""

import os

from fly import config
from fly.translation import wordstochords


class LessonToChords(object):

    """Lesson converted to chords so that chords user must type are known."""

    CHORDS_FILE_EXTENSION = '.chd'

    def __init__(self, dictionary): 

        """
        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        self.translator = wordstochords.WordToChordTranslator(dictionary)

    def get_chords_file_path(self, lesson_file_path):
        
        """Read or create chords file and return path to file.
        
        @param lesson_file_path: file path to lesson to read/create chords for.
        @type lesson_file_path: str
        """

        chords_file_path = '%s%s' % (os.path.splitext(lesson_file_path)[0], 
                                     self.CHORDS_FILE_EXTENSION)
        
        if config.FORCE_LESSON_REGENERATION or \
           not os.path.exists(chords_file_path):
            self.__generate_chords(lesson_file_path, chords_file_path)

        return chords_file_path

    def __generate_chords(self, lesson_path, chords_file_path):
        
        """Generate chords and write to file.

        @param lesson_path: file path to lesson
        @param chords_file_path: file path to chords file corresponding to
                                 lesson file.

        @type lesson_path: str
        @type chords_file_path: str
        """

        chord_lines_list = self.translator.translate_from_file(lesson_path)
        chord_lines = '\n'.join(chord_lines_list)
        with open(chords_file_path, 'w') as f:
            f.write(chord_lines)


