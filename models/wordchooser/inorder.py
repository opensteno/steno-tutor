# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Retrieve the lesson in order, first word, then second word and so on."""

import re

from fly.models.wordchooser import interface


class RetrieveInOrder(interface.WordChooserInterface):

    """Retrieve words in order, looping back to the first at the end."""

    def __init__(self, word_translation_dict, word_list):

        """
        @param word_translation_dict: dict mapping steno chord to 
                                      english translation for every
                                      chord in word_list
        @param word_list: list of steno words to present to user

        @type word_translation_dict: dict
        @type word_list: list
        """

        self.index = 0
        self.word_translation_dict = word_translation_dict
        self.word_list = word_list

    def get_word_and_translation(self, level):

        if self.index >= len(self.word_list):
            self.index = 0

        word = self.word_list[self.index]
        self.index += 1
        translation = self.word_translation_dict[word]
        return word, translation

    def get_current_word_index(self):
        return self.index - 1


class RetrieveInOrderSentence(interface.WordChooserInterface):

    """Retrieve words in order, but display sentence for context."""

    def __init__(self, lesson):
        
        """
        @param lesson: lesson object to add directives to
        @type lesson: L{lessons.container.Lesson}
        """

        self.lesson = lesson
        self.index = 0
        self.sentence_ind = 0
        self.retriever = RetrieveInOrder(lesson.chord_translation_dict, 
                                         lesson.chords_list)

    def get_word_and_translation(self, level):

        word, translation = self.retriever.get_word_and_translation(level)
        self.index = self.retriever.get_current_word_index()
        return word, translation
    
    def get_display_word_and_translation(self, level):

        for sentence_ind, word_inds in self.lesson.sentence_map.iteritems():
            if self.index in word_inds:
                self.sentence_ind = sentence_ind
                return self.lesson.chord_sentences_list[sentence_ind], \
                       self.lesson.sentences_list[sentence_ind]
    
    def return_inputs(self, input_word, input_translation):

        chord_sentence = self.lesson.chord_sentences_list[self.sentence_ind]
        chord_sentence = self.__match_sentence(self.lesson.chords_list,
                                               chord_sentence,
                                               input_word)

        translation_sentence = self.lesson.sentences_list[self.sentence_ind]
        trans_sentence = self.__match_sentence(self.lesson.translation_list,
                                               translation_sentence,
                                               input_translation)

        return chord_sentence, trans_sentence 

    def __match_sentence(self, to_type_list, sentence, new_input):

        """Match input word against the sentence expected to be typed.
        Return the sentence with the new word appended. Doing it this way 
        means that the word is added with correct capitalization and spacing 
        regardless of the circumstances, which is cheating, but nice and easy.
        
        @param to_type_list: chords to type
        @param sentence: steno sentence to type
        @param new_input: steno word

        @type to_type_list: list of str
        @type sentence: str
        @type new_input: str

        @return: sentence with new word appended
        @rtype: str
        """

        input_sentence = new_input

        match_str = ""
        for i in self.lesson.sentence_map[self.sentence_ind]:
            if i > self.index - 1:
                break
            input = re.sub("\*", "\*", to_type_list[i])
            match_str += "%s\s*" % input

        if match_str:
            matchObj = re.match(match_str, sentence, re.IGNORECASE)
            if matchObj:
                input_sentence = matchObj.group(0) + new_input
       
        return input_sentence


