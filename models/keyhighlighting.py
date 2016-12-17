# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""
Interpret steno word to figure out which qwerty keys should be pressed.

This module deals with keys that should be highlighted to indicate to the user 
the keys that need to be pressed.
"""

from fly.data import stenoqwerty
from fly.data import alphabetdict as alphabet
from fly.translation import ploverfacade

import logging
logger = logging.getLogger(__name__)


class KeyHighlighterInterface(object):
    
    """
    Defines an interface for a class that gets keys to type given 
    steno word to type and what has been typed.
    """

    def get_qwerty_letters_to_type(self, word, input_word):

        """Return qwerty letters corresponding to word to type.

        @param word: the steno keys that need to be pressed
                     in order to generate the word the user needs to type.
        @param input_word: the steno keys that the user has pressed already.
        
        @type word: str
        @type input_word: str

        @return: list of qwerty letters. In the list, one entry may correspond
                 to multiple qwerty letters, for example if the steno letter is
                 "S" then "QA" will be in the list.
        @rtype: list of string
        """

        pass


class KeyHighlighter(KeyHighlighterInterface):

    """
    A class that gets keys to type given steno word to type and what has 
    been typed already.
    """
    
    def get_qwerty_letters_to_type(self, word, input_word):
        steno_word = self.get_stroke(word, input_word)
        real_letters = self.get_real_letters(steno_word)
        qwerty_letter_list = self.get_qwerty_letter_list(real_letters)
        return qwerty_letter_list
    
    def get_stroke(self, steno_word, input_word):

        """For multichorded words, return the chord the user needs to type.
        
        If the user has typed in the first stroke, present them with the 
        second and so on. Even if the first is incorrect, the second chord
        should be returned.
       
        @param steno_word: word to type in steno letters, e.g. AU/ROR/RA
        @param input_word: what user has typed already in steno letters, 
                           e.g. ROR

        @type steno_word: str
        @type input_word: str

        @return: chord which user must type, subset of steno_word.
        @rtype: str
        """

        split_word = steno_word.split('/')
        input_split = input_word.split('/')

        # Make the input_split list length match the split_word list length.
        for i in range(len(split_word)):
            if len(input_split) <= i:
                input_split.append(None)

        for word, input in zip(split_word, input_split):
            if word == input:
                continue
            else:
                return word
        
        return split_word[0]
        
    def get_real_letters(self, steno_word):

        """Return list of steno letters typed (different from chord-to-type).

        steno_word contains steno letters which might not represent the actual
        keys being pressed. For example, -PBLG is really -P -B -L -G, since all
        letters are on the right. More examples in test_keyhighlighting.

        @param steno_word: single chord word to type in steno letters, 
                           e.g. AU
        @type steno_word: str

        @return: list of steno keys.
        @rtype: list of str
        """

        previous_letter_order = 0
        real_letters = []
        word_starter = ''

        for letter in steno_word:
            if letter == '-':
                word_starter = '-'
                continue
            real_letters_left = self.__get_real_letters_left(letter)
            real_letters_right = self.__get_real_letters_right(letter)
            results = self.__pick_side(real_letters_left, 
                                       real_letters_right, 
                                       word_starter,
                                       previous_letter_order,
                                       steno_word)
            if not results:
                continue
            real_letter = results[0]
            letter_order = results[1]
            previous_letter_order = letter_order 
            real_letters.append(real_letter)
        return real_letters

    def __pick_side(self, letters_left, letters_right, 
                    word_starter, previous_letter_order, steno_word):

        """Decide whether left or right letters should be used.
        
        @param letters_left: the steno letters as would appear on LHS 
                             of keyboard.
        @param letters_right: the steno letters as would appear on RHS
                              of keyboard.
        @param word_starter: '-' or '' to potentially indicate side of keyboard
        @param previous_letter_order: the order of the steno key/s on the 
                                      keyboard for the previous steno key/s
                                      in the chord.
        @param steno_word: single chord word to type in steno letters, 
                           e.g. AU

        @type letters_left: str
        @type letters_right: str
        @type word_starter: str
        @type previous_letter_order: int
        @type steno_word: str

        @return: tuple of (letters_left or letters_right, how far right on the
                 keyboard the letters go, according to steno ordering)
        @rtype: (str, int)
        """

        if word_starter:
            right_ordering = self.__get_ordering(letters_right, 
                                                 previous_letter_order)
            return letters_right, self.__get_max(right_ordering, steno_word)

        left_ordering = self.__get_ordering(letters_left, 
                                            previous_letter_order)
        right_ordering = self.__get_ordering(letters_right, 
                                             previous_letter_order)

        if len(left_ordering) != 0 and len(right_ordering) != 0:
            return letters_left, self.__get_max(left_ordering, steno_word)

        if len(left_ordering) == 0 and len(right_ordering) != 0:
            return letters_right, self.__get_max(right_ordering, steno_word)

        if len(left_ordering) != 0:
            return letters_left, self.__get_max(left_ordering, steno_word)
        return None
            
    def __get_max(self, letter_order_list, steno_word):
        
        """Get max of list or raise exception on empty list."""

        if letter_order_list is []:
            excStr = "Bug detected! Steno chord %s caused this error. "\
                     "Please report this bug following instructions "\
                     "in the README file which can be found in Fly's main "\
                     "dir. Include this error "\
                     "message." % steno_word
            raise Exception(excStr)
        return max(letter_order_list)

    def __get_ordering(self, letters, previous_letter_order):

        """Return list of ints representing the order of the letters.

        The order of the letters is determined by the structure of the
        steno keyboard.

        @param letters: letters to get ordering for
        @param previous_letter_order: maximum letter order for previous letters

        @type letters: str
        @type previous_letter_order: int

        @return: list of letter orders 
        @rtype: list of int
        """

        letter_order_list = []
        word_starter = ''
        for letter in letters:
            if letter == '-':
                word_starter = letter
                continue
            letter_order = ploverfacade.get_ordering(word_starter + letter)
            if letter_order >= previous_letter_order:
                letter_order_list.append(letter_order)
        
        return letter_order_list

    def __get_real_letters_left(self, letter):

        """Assuming letter is on the left, return steno key/s to press.

        @param letter: steno letter
        @type letter: str

        @return: steno keys
        @rtype: str
        """

        if letter in alphabet.STENO_ALPHABET:
            return alphabet.STENO_ALPHABET[letter] 
        return ''
    
    def __get_real_letters_right(self, letter):

        """Assuming letter is on the right, return steno_key/s to press.
        
        @param letter: steno letter
        @type letter: str
        
        @return: steno keys
        @rtype: str
        """

        if '-%s' % letter in alphabet.STENO_ALPHABET:
            return alphabet.STENO_ALPHABET['-%s' % letter] 
        return ''

    def get_qwerty_letter_list(self, real_letters):

        """Translate list of steno keys to list of qwerty keys to press.

        A steno key might map to more than one qwerty case. In this case, there
        will be multiple keys in a string. For examples see 
        keyhighlighting_test.

        @param real_letters: Each steno letter to press.
        @type real_letters: list of str

        @return: list of qwerty letters (list may have entries with multiple
                 letters, e.g. steno S maps to qwerty QA)
        @rtype: list of str
        """

        qwerty_letter_list = []
        for letters in real_letters:
            word_starter = ''
            for key in letters:
                if key == '-':
                    word_starter = key
                    continue
                qwerty_letters = stenoqwerty.STENO_TO_QWERTY[word_starter + key]
                qwerty_letter_list.append(qwerty_letters)

        return qwerty_letter_list


