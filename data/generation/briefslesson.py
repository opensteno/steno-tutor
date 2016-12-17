# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

"""
Code to generate a lesson file containing only briefs.

This is done by extracting all briefs from word_category dictionary.

Call from main game directory to regenerate briefs lesson:
    python -m data.generation.briefslesson
"""

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import fly.utils.files as fileutils
import fly.utils.dictionaryreader as dictionaryreader
from fly.translation import wordstochords


class BriefsLessonCreator(object):

    """
    Given a word_category dictionary, extract all chords with category "brief"
    into a lesson file.
    """

    word_cat_dict_filename = fileutils.get_categorization_dict_path()

    def __init__(self, dictionary):

        """
        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        self.dict = dictionary
    
    def __call__(self, output_filename_les, output_filename_chd):
        
        """Do it!"""

        chord_list = []

        word_cat_dict = dictionaryreader.load_dict(self.word_cat_dict_filename)

        for word, category in word_cat_dict.iteritems():
            if category == wordstochords.BRIEF:
                chord_list.append(word)
    
        chords_in_dict_list = []
        with open(output_filename_les, 'w') as f:
            for chord in chord_list:
                if chord in self.dict:
                    f.write(self.dict[chord] + "\n")
                    chords_in_dict_list.append(chord)
                else:
                    logger.warning("Chord %s not found in dict!" % chord)

        with open(output_filename_chd, 'w') as f:
            f.write("\n".join(chords_in_dict_list))


if __name__ == "__main__":

    lessons_dir = fileutils.get_lessons_directory()
    output_file_les = os.path.join(lessons_dir, "briefs.les")

    # Why do we have to generate the chd file instead of letting this happen
    # automatically? Because if it happens automatically it will be looking
    # for canon chords preferentially, but on this occasion we want briefs.
    output_file_chd = os.path.join(lessons_dir, "briefs.chd")

    dict_filepath = fileutils.get_plover_dict_path()
    dictionary = dictionaryreader.load_dict(dict_filepath)

    # Generate lessons/briefs.chd
    logger.info("Generating files: %s, %s..." % (output_file_les, 
                                                 output_file_chd))

    briefs_lesson_creator = BriefsLessonCreator(dictionary)
    briefs_lesson_creator(output_file_les, output_file_chd)

    logger.info("Done.")


