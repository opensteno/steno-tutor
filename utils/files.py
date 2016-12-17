# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Provides file path information about files in Fly."""

import os


def get_base_directory():
    """Get the main directory of the game."""
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_dictionaries_directory():
    """Return the directory which contains dictionaries."""
    return os.path.join(get_base_directory(), 'data', 'dicts')


def get_plover_dict_path():
    """Return the file path of the plover dictionary."""
    return os.path.join(get_dictionaries_directory(), 'dict.json')


def get_level_dict_path(level):
    """Return the file path to the level dict specified."""
    return os.path.join(get_dictionaries_directory(),
                        'dict_level_%s.json' % level)

def get_categorization_dict_path():
    """Return the file path to the categorization dict."""
    return os.path.join(get_dictionaries_directory(),
                        'word_category.json')

def get_lessons_directory():
    """Get the directory with the lesson files."""
    return os.path.join(get_base_directory(), 'data', 'lessons')


def get_test_data_directory():
    """Return the file path to the directory containing test data."""
    return os.path.join(get_base_directory(), 'tests', 'data')

def get_lesson_words_categories_dict_path():
    """Return the file path to the word:category dict for the lessons."""
    return os.path.join(get_dictionaries_directory(), 
                        'word_category.json')

