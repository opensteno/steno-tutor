# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Data class for a lesson."""


class Lesson(object):
    def __init__(self, name, nice_name, file_path):
        self.name = name 
        self.nice_name = nice_name 
        self.file_path = file_path

        self.chords_file_path = None
        self.retrieval_directive = None
        self.display_directive = None

        self.chords_list = []
        self.translation_list = []
        self.chord_translation_dict = {}
        self.sentences_list = []
        self.chord_sentences_list = []
        self.sentence_map = {}

    def __repr__(self):
        return 'Lesson %s: \n\t\
                nice name: %s\n\t\
                file path: %s\n\t\
                chords file path: %s\n\t\
                retrieval directive: %s\n\t\
                display directive: %s\n\t\
                chords list: %s\n\t\
                translation list: %s\n\t\
                chord translation dict: %s\n\t\
                sentences list: %s\n\t\
                chord sentences list: %s\n\t\
                sentence map: %s\n\t\
                ' % (self.name, self.nice_name, self.file_path, 
                     self.chords_file_path, self.retrieval_directive, 
                     self.display_directive, self.chords_list, 
                     self.translation_list, self.chord_translation_dict,
                     self.sentences_list, self.chord_sentences_list, 
                     self.sentence_map)

    def __eq__(self, other):
        return self.name == other or self.nice_name == other


