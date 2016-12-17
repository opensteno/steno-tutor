# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

"""
Code to generate dictionaries based on filtering.

This module contains classes to generate dictionaries based on how
easy it is to type the chords required to spell the words. The difficulty
increases from Level 1 to Level 6.

Call from main game directory to regenerate dictionaries:
    python -m data.generation.leveldictextraction
"""

import json
import re

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import fly.utils.files as fileutils
import fly.utils.dictionaryreader as dictionaryreader


class LevelDictionaryCreator(object):

    """
    Given a complete dictionary, filter to create 6 dictionaries
    with words of different difficulty level.
    """

    dictionary_filename_1 = fileutils.get_level_dict_path(1)
    dictionary_filename_2 = fileutils.get_level_dict_path(2)
    dictionary_filename_3 = fileutils.get_level_dict_path(3)
    dictionary_filename_4 = fileutils.get_level_dict_path(4)
    dictionary_filename_5 = fileutils.get_level_dict_path(5)
    dictionary_filename_6 = fileutils.get_level_dict_path(6)
    
    def __init__(self, dictionary):

        """
        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        self.dictionary = dictionary

    def dump_dicts(self):

        """Generates and writes out 6 dicts to hard-coded relative filepaths"""

        sixDict = self.get_level_six_dict(self.dictionary)    
        dump(sixDict, self.dictionary_filename_6)

        fiveDict = self.get_level_five_dict(sixDict)
        dump(fiveDict, self.dictionary_filename_5)

        fourDict = self.get_level_four_dict(fiveDict)
        dump(fourDict, self.dictionary_filename_4)

        threeDict = self.get_level_three_dict(fourDict)
        dump(threeDict, self.dictionary_filename_3)

        twoDict = self.get_level_two_dict(threeDict)
        dump(twoDict, self.dictionary_filename_2)

        oneDict = self.get_level_one_dict(twoDict)
        dump(oneDict, self.dictionary_filename_1)


    @staticmethod
    def get_level_six_dict(dictionary):

        """Generate hardest dict. All curly braces and numbers filtered.

        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        level_dict = {}
        for key, value in dictionary.iteritems():
            if value.find("{") != -1:
                continue
            
            level_dict[key] = value
        return level_dict
    
    @staticmethod
    def get_level_five_dict(dictionary):

        """Generate 5th easiest dictionary (2nd hardest). No capitalized words.

        @param dictionary: prefiltered dict that has passed through level 6. 
        @type dictionary: dict
        """

        level_dict = {}
        for key, value in dictionary.iteritems():
            if value.lower() != value:
                continue

            level_dict[key] = value
        return level_dict        

    @staticmethod
    def get_level_four_dict(dictionary):

        """Generate fourth easiest dictionary. Two chords only, no numbers.

        @param dictionary: prefiltered dict that has passed through other two
                           levels. 
        @type dictionary: dict
        """

        level_dict = {}
        for key, value in dictionary.iteritems():
            if len(re.sub('[\w*]', '', key)) > 1: 
                continue

            level_dict[key] = value
        return level_dict        

    @staticmethod
    def get_level_three_dict(dictionary):

        """Generate third easiest dictionary. One chord only, any length.

        @param dictionary: prefiltered dict that has passed through other three
                           levels. 
        @type dictionary: dict
        """

        level_dict = {}
        for key, value in dictionary.iteritems():
            if key.find('/') != -1:
                continue

            level_dict[key] = value
        return level_dict        

    @staticmethod
    def get_level_two_dict(dictionary):

        """Generate second easiest dictionary. 4 keys or less.

        @param dictionary: prefiltered dict that has passed through other four
                           levels. 
        @type dictionary: dict
        """

        level_dict = {}
        for key, value in dictionary.iteritems():
            if len(key.lstrip('-')) > 4:
                continue

            level_dict[key] = value
        return level_dict        

    @staticmethod
    def get_level_one_dict(dictionary):

        """Generate easiest dictionary. 2 keys or less. 

        @param dictionary: prefiltered dict that has passed through other five
                           levels. 
        @type dictionary: dict
        """

        level_dict = {}
        for key, value in dictionary.iteritems():
            if len(key.lstrip('-')) > 2:
                continue

            level_dict[key] = value
        return level_dict        


def dump(dictionary, filepath):

    """Write dictionary to filepath.

    @param dictionary: plover keystroke to translation dict
    @param filepath: path of file to write dict to

    @type dictionary: dict
    @type filepath: str
    """
    
    with open(filepath, 'w') as f:
        logger.info("Writing %s" % filepath)
        json.dump(dictionary, f)


def writeFilteredDict(dictionary, dict_filepath):

    """Customize plover's default dictionary for use with Fly.

    @param dictionary: plover keystroke to translation dict
    @param filepath: path of file to write dict to

    @type dictionary: dict
    @type filepath: str
    """

    new_dictionary = {}

    for key, value in dictionary.iteritems():
        # Chords containing numbers are currently not supported. When they 
        # are, perhaps move this to Level 4 to introduce numbers earlier.
        if re.search('\d', key) != None:
            continue

        new_dictionary[key] = value
        
    # Removing "he is" from dictionary since the two strokes are defined
    # separately ("he": "E", "is": "S"). They're an artifact from some 
    # proprietary software's "Translation Magic" algorithm.
    if "E/S" in new_dictionary:
        new_dictionary.pop("E/S")
    dump(new_dictionary, dict_filepath) 

    dictionary = new_dictionary


if __name__ == "__main__":

    # Filter main plover dict to write 6 dictionaries of varying difficulty
    logger.info("Generating dictionaries...")

    dict_filepath = fileutils.get_plover_dict_path()
    dictionary = dictionaryreader.load_dict(dict_filepath)

    writeFilteredDict(dictionary, dict_filepath)

    level_dict_creator = LevelDictionaryCreator(dictionary)
    level_dict_creator.dump_dicts()

    logger.info("Done.")


