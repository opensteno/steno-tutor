# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""
The lessons directory contains lesson files (extension .les) and chord files
(extension .chd). Chord files are generated if they don't exist. Lesson files
are plain text files with directive in first line. See file 
HOW_TO_ADD_LESSONS in data/lessons for more info.
"""

from fly.lessons.helpers.finder import LessonFinder
from fly.lessons.helpers.tochords import LessonToChords
from fly.lessons.helpers.directive import DirectiveInterpreter
from fly.lessons.helpers.filler import LessonFiller
from fly.lessons.helpers.mapper import LessonWordChooserMapper
from fly.utils import files as fileutils


class LessonControl(object):

    """Deals with reading lesson from text file and translating."""

    def __init__(self, dictionary):
        
        """
        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        self.current_lesson = None
        self.dir_helper = LessonFinder(fileutils.get_lessons_directory())
        self.chord_helper = LessonToChords(dictionary)
        self.populate_helper = LessonFiller()
        self.word_chooser_helper = LessonWordChooserMapper()
        
        self.lesson_list = self.dir_helper.find_lessons()
        for lesson in self.lesson_list:
            self.__add_directives_to_lesson_obj(lesson)
            self.__add_chords_to_lesson(lesson.file_path, lesson)

    def __add_directives_to_lesson_obj(self, lesson):

        """Read directives from lesson file and add to lesson object.

        Directives are specified at the top of the lesson file and contain
        information about how the lesson should be presented.

        @param lesson: lesson object to add directives to
        @type lesson: L{lessons.container.Lesson}
        """

        first_line = ""
        with open(lesson.file_path) as f:
            first_line = f.readline().strip()
        interpreter = DirectiveInterpreter(first_line)
        lesson.retrieval_directive = interpreter.get_retrieval_directive()
        lesson.display_directive = interpreter.get_display_directive()

    def __add_chords_to_lesson(self, lesson_path, lesson):    

        """Generate/read the steno chords that correspond to the lesson.
        
        If the chords file exists, use that. Otherwise generate one. Add
        the chords file path to the lesson.
        
        @param lesson_path: path to lesson file.
        @param lesson: lesson object to add chords to.
        
        @type lesson_path: str
        @type lesson: L{lessons.container.Lesson}
        """
        
        chords_file_path = self.chord_helper.get_chords_file_path(lesson_path)
        lesson.chords_file_path = chords_file_path

    def get_lesson_names(self):

        """Return a list of nice lesson names from the lessons found.

        @return: list of nice lesson names
        @rtype: list of str
        """

        return [lesson.nice_name for lesson in self.lesson_list] 

    def get_lesson(self, name):

        """Given a lesson name return lesson object with that name, or None.

        @return: lesson object for lesson with name as specified.
        @rtype: {lessons.container.Lesson}
        """

        for lesson in self.lesson_list:
            if lesson.name == name or lesson.nice_name == name:
                return lesson
    
    def get_word_chooser(self, lesson_name):

        """Get a word chooser that is appropriate for presenting the lesson.
        
        For example, if the lesson has retrieval directive "randomize", get
        a word chooser that will present lesson content in a random order.

        @param lesson_name: lesson name to get chooser for. Can be name
                            or nice name.
        @type lesson_name: str
        """

        lesson = self.get_lesson(lesson_name)
        if self.current_lesson == lesson:
            return 

        self.populate_helper.populate_lesson(lesson)
        word_chooser = self.word_chooser_helper.get_word_chooser(lesson)
        self.current_lesson = lesson

        return word_chooser

        
