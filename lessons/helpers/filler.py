# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Populates lesson object by reading lesson files and interpreting data."""

import re
import logging
logger = logging.getLogger(__name__)

from fly.translation import wordstochords


class LessonFiller(object):

    """Reads lesson and chords file and populates lesson with information."""

    def populate_lesson(self, lesson):

        """Read the files belonging to the lesson to populate the lesson.

        @param lesson: lesson object to populate.
        @type lesson: L{lessons.container.Lesson}
        """

        # Read lesson and chords file to get lists of content, store on lesson
        translation_sentence_list = self.get_sentences_list(lesson.file_path)
        lesson.sentences_list = translation_sentence_list

        chord_sentence_list = self.get_sentences_list(lesson.chords_file_path)
        lesson.chord_sentences_list = chord_sentence_list

        chords_list = self.get_chords_list(lesson)
        lesson.chords_list = chords_list

        # Generate a translation list, which has punctuation split out as well,
        # and a map so we know which sentence each chord belongs to.
        lesson.translation_list, lesson.sentence_map =\
            self.generate_translation_for_sentences(translation_sentence_list)
        
        # For convenience, map from chord to translation.
        lesson.chord_translation_dict = self.get_translation_dict(lesson)

    @staticmethod
    def get_chords_list(lesson):

        """Get a list of chords from the chords file.

        @param lesson: lesson object which knows about chord file path
        @type lesson: L{lessons.container.Lesson}

        @return: list of chords
        @rtype: list of str
        """
        
        with open(lesson.chords_file_path) as f:
            chords_list = f.read().split()
            chords_list = [s.strip() for s in chords_list]

        return chords_list

    @staticmethod
    def get_sentences_list(file_path):
        
        """Get a list of sentences from the file.

        For example, might return something like ["roses are red", "violets 
        are blue"]

        @param filePath: path to file containing sentences
        @type filePath: str

        @return: list of sentences
        @rtype: list of str
        """

        sentence_list = []

        with open(file_path) as f:
            split_list = f.read().split('\n')

        for line in split_list:
            if line.find("<") != -1 or line.find(">") != -1:
                continue
            if line == "":
                continue

            sentence_list.append(line)
        return sentence_list

    @classmethod
    def generate_translation_for_sentences(cls, translation_sentence_list):

        """Generate a list of chords and a map from sentence to chord.

        @param translation_sentence_list: list of sentences
        @type translation_sentence_list: list of str

        @return: tuple (list of word translations, dict of sentence
                 number to list of indices in translation list which correspond
                 to sentence)

        @rtype: tuple (list of string, dict of int: list of int.)
        """

        final_translations_list = []
        sentence_map = {}
        total_word_count = 0
        i = 0

        for sentence in translation_sentence_list:
            word_count = 0
            translation_list = cls.get_translations_from_sentence(sentence)

            for word in translation_list:
                split_words = re.split("([-.,?!:;\"])", word)
                words_and_punctuation = [w for w in split_words if w is not ""]
                final_translations_list.extend(words_and_punctuation)
                word_count += len(words_and_punctuation)
                total_word_count += len(words_and_punctuation)

            if word_count == 0:
                continue

            word_indices = cls.generate_word_indices(word_count, 
                                                     total_word_count)
            sentence_map[i] = word_indices
            i += 1

        return final_translations_list, sentence_map

    @staticmethod
    def get_translations_from_sentence(sentence):

        """Split sentence into words and reject directives.

        @param sentence: translated sentence to split
        @type sentence: str

        @return: list of words in sentence, with punctuation still attached.
        @rtype: list of str
        """

        translation_list = sentence.split()
        valid_translation_list = []
        for t in translation_list:
            # Directives are not allowed
            if t.find("<") != -1 or t.find(">") != -1:
                continue

            t = t.lower().strip()
            valid_translation_list.append(t)

        return valid_translation_list

    @staticmethod
    def generate_word_indices(word_count, total_word_count):

        """Generate indices for word_count words up to total_word_count.

        @param word_count: number of words to generate indices for
        @param total_word_count: number of words seen so far including 
                                 words in word_count.

        @type word_count: int
        @type total_word_count: int

        @return: list of word indices
        @rtype: list of int
        """

        end = total_word_count - 1
        start = total_word_count - word_count
        index = start
        word_indices = []
        while index <= end:
            word_indices.append(index)
            index += 1

        return word_indices

    @staticmethod
    def get_translation_dict(lesson):

        """Create a dict of chord: translation for lesson data.

        @param lesson: lesson object
        @type lesson: L{lessons.container.Lesson}

        @return: dict of chord: translation
        @rtype: dict of str: str 
        """

        word_getter = wordstochords.WordToChordTranslator.yield_word
        translation_list = []
        
        with open(lesson.file_path) as f:
            data = f.readlines()
            for line in data:
                for word in word_getter(line):
                    translation_list.append(word)

        chord_translation_dict = {}
        for chord, translation in zip(lesson.chords_list, translation_list):
            chord_translation_dict[chord] = translation
        return chord_translation_dict


