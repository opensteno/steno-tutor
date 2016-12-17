# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Alter plover's steno and translation for alphabet mode."""

from fly.models.inputinterpreter import interface
from fly.data import alphabetdict


class InterpretForAlphabet(interface.InputInterpreter):

    """Alters what plover says word translates to for alphabet."""

    def run(self, input_word, word_to_type, 
            current_input_word, input_translation):

        """
        Retranslate user input word to be steno alphabet letter. For example,
        if steno word user typed was "S" that would be "is" in the plover dict.
        But in teaching the user the alphabet it should translate to "S"
       
        Param docs in interface.InputInterpreter.
        """

        return_input_word = None
        return_input_translation = None

        if input_translation is "":
            return return_input_word, return_input_translation 

        # Multi-strokes not supported in alphabet mode
        input_word = input_word.split('/')[-1]

        return_input_word = input_word
        if input_word in alphabetdict.INVERSE_STENO:
            return_input_translation = alphabetdict.INVERSE_STENO[input_word]
        else:
            return_input_translation = input_translation
        
        return return_input_word, return_input_translation 



