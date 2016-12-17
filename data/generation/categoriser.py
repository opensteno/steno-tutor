#!/usr/bin/python
# Copyright (c) 2012 Pragma Nolint.
# See LICENSE.txt for details.

"""Command line script for helping users categorise words in lessons.

Prompts user to classify chords into categories such as
canon, alternative and misstrokes. This information will be stored in fly/
data/dicts/word_category.json.
Call from the fly directory with the following command:
    python -m data.generation.categoriser
"""

import os
import sys
import json

# Hack so that all modules can be imported from Fly, 
# but this can be called as a script
sys.path.append(os.path.dirname(os.getcwd()))

from fly.utils import files as fileutils
from fly.utils import dictionaryreader
from fly.lessons.helpers import finder
from fly.lessons.helpers.filler import LessonFiller
from fly.lessons.helpers.tochords import LessonToChords
from fly.translation import wordstochords


def get_all_words_in_lessons(dictionary):

    """Get a unique list of all english words in Fly lessons.
    
    @param dictionary: plover keystroke to translation dict
    @type dictionary: dict

    @return: list of words
    @rtype: list of str
    """

    word_list = []

    # Find lessons from fly's lesson directory
    lessons_dir = fileutils.get_lessons_directory()
    lesson_finder = finder.LessonFinder(lessons_dir)
    lesson_list = lesson_finder.find_lessons()
    
    # Populate lesson objects
    lesson_filler = LessonFiller()
    chord_helper = LessonToChords(dictionary)

    for lesson in lesson_list:
        chords_file_path = chord_helper.get_chords_file_path(lesson.file_path)
        lesson.chords_file_path = chords_file_path
        lesson_filler.populate_lesson(lesson)
        word_list.extend(lesson.translation_list)

    # Remove duplicate entries
    word_list = list(set(word_list))
    
    return word_list


def get_words_to_categorise(dictionary, word_list, category_dict):

    """Translate words, and exclude if they have already been categorised
    or if they don't need to be categorised as they only have one entry in the
    dict. 

    @param dictionary: plover keystroke to translation dict
    @param word_list: list of english words (no duplicate entries) to 
                      categorise 
    @param category_dict: dict of already categorised words (steno chord to 
                          category).
     
    @type dictionary: dict
    @type word_list: list of str
    @type category_dict: dict of str: str.
    
    @return: dict of english word to ChordHolder object
    @rtype: dict of str: L{fly.translation.wordstochords.ChordHolder}
    """

    translator = wordstochords.WordToChordTranslator(dictionary)
    inverse_dict = translator.inverse_dict

    word_chord_holder_dict = {}
    for word in word_list:
        first_try_handler = wordstochords.WordAsIs(inverse_dict)
        second_try_handler = wordstochords.WordLowerCase(inverse_dict)
        default_handler = wordstochords.WordUndefined(inverse_dict)
        
        first_try_handler.successor = second_try_handler
        second_try_handler.successor = default_handler

        # Translate word--get all chords corresponding to word
        chord_holder = first_try_handler.handle(word)
        chord_list = []

        # Only process if there's more than one chord found.
        if chord_holder and len(chord_holder.chord_list) > 1:
            for chord in chord_holder.chord_list:
                if chord not in category_dict:
                    chord_list.append(chord)
        if len(chord_list) > 0:
            word_chord_holder_dict[word] = wordstochords.ChordHolder(chord_list)
    return word_chord_holder_dict


def find_option(option):

    """Translate what user has typed to a valid option if possible.

    @param option: user input
    @type option: str

    @return: category user has specified through their choice of option
    @rtype: str
    """

    nominated_option = None
    if option.find("c") != -1:
        nominated_option = wordstochords.CANON

    if option.find("a") != -1:
        nominated_option = wordstochords.ALTERNATIVE

    if option.find("b") != -1:
        nominated_option = wordstochords.BRIEF
        
    if option.find("m") != -1:
        nominated_option = wordstochords.MISSTROKE

    if option.find("u") != -1:
        nominated_option = wordstochords.UNKNOWN

    return nominated_option


def exit(category_dict_path, category_dict, new_category_dict):

    """Always save prior to exiting, and print where the dict has been saved.

    @param category_dict_path: file path to category dict (can exist, will be
                               overwritten)
    @param category_dict: old category dict that existed when user started
                          session
    @param new_category_dict: category dict user has created during session.

    @type category_dict_path: str
    @type category_dict: dict
    @type new_category_dict: dict
    """

    category_dict.update(new_category_dict)
    with open(category_dict_path, 'w') as f:
        print("Saving dict to %s" % category_dict_path)
        json.dump(category_dict, f)

    print("Exiting...")
    return


def main():

    """Starts an interactive command line session asking user to categorise
    lesson words until there are none left to categorise."""

    # Generate plover dict
    dict_filename = fileutils.get_plover_dict_path()
    print("Loading plover dict...")
    dictionary = dictionaryreader.load_dict(dict_filename)

    # Get words from lessons
    lessons_dir = fileutils.get_lessons_directory()
    print("Reading lessons from %s..." % lessons_dir)
    word_list = get_all_words_in_lessons(dictionary)
  
    # Get or create category dictionary
    category_dict_path = fileutils.get_lesson_words_categories_dict_path()
    if os.path.exists(category_dict_path):
        category_dict = dictionaryreader.load_dict(category_dict_path)
        print("Existing category dictionary contains %s entries, new "
              "entries will be added to it." % len(category_dict.keys()))
    else:
        print("No existing category dictionary found, "
              "creating new dict.")
        category_dict = {}

    # Find steno chords from english words, and filter out already categorised
    # (also, if there's only one chord, don't need to categorise). 
    word_chord_holder_dict = get_words_to_categorise(dictionary, word_list, category_dict)
    all_chords = []
    for word, chord_holder in word_chord_holder_dict.iteritems():
        all_chords.extend(chord_holder.chord_list)

    # Filter word list to exclude those that have already been categorised
    print("%s uncategorised chords (%s words) found in "
          "lessons files." % (len(all_chords), len(word_chord_holder_dict.keys())))


    # Query user for each chord for multiple chorded words in filtered word list
    option_str = "Please choose one of: c) %s a) %s b) %s " \
                 "m) %s u) %s (q to quit)" % (wordstochords.CANON, 
                                              wordstochords.BRIEF, 
                                              wordstochords.MISSTROKE, 
                                              wordstochords.UNKNOWN)

    new_category_dict = {} 
    for word, chord_holder in word_chord_holder_dict.iteritems():
        print("_______________________________________________")
        print("Word \"%s\" has %s chords: %s" % (word,
                                                 len(chord_holder.chord_list), 
                                                 chord_holder))
        
        for chord in chord_holder.chord_list:
            print("\n" + option_str)
            request_option_str = "[word: %s] %s: " % (word, chord)

            # Get user input
            option = raw_input(request_option_str)
            if option.find("q") != -1:
                # Save dict and quit
                exit(category_dict_path, category_dict, new_category_dict)
                return

            # Figure out which option was nominated
            nominated_option = find_option(option)
            
            # Handle invalid options by asking again
            while not (nominated_option):
                print("Invalid input: %s" % option)
                print(option_str)
                option = raw_input(request_option_str)
                if option.find("q") != -1:
                    # Save dict and quit
                    exit(category_dict_path, category_dict, new_category_dict)
                    return
                
                nominated_option = find_option(option)
            
            # Put user response into dictionary
            print("%s => %s" % (chord, nominated_option))
            new_category_dict[chord] = nominated_option

    # Out of words.
    print("No more words to process.")
    exit(category_dict_path, category_dict, new_category_dict)


if __name__ == '__main__':
    main()


