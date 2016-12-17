# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Alter plover's steno and translation for word mode."""

from fly.models.inputinterpreter import interface


class InterpretForWord(interface.InputInterpreter):

    """Alters what plover says word translates to for multistrokes."""

    def run(self, input_word, word_to_type, 
            current_input_word, input_translation):
        
        """
        Keep track of previous strokes for multistroke word support.

        Add previous strokes if the input_word is a continuation of them
        E.g. if A/B and user has typed C, C shouldn't be returned as the 
        steno word user has typed. Rather, we want A/B/C, but only if 
        this matches what the user should type (the word to type).

        Param docs in interface.InputInterpreter.
        """

        if input_translation is "":
            return None, None

        if current_input_word:
            final_input_stroke = input_word.split('/')[-1]
            proposed_input = '/'.join([current_input_word, final_input_stroke])
            if word_to_type.find(proposed_input) != -1:
                return proposed_input, input_translation
        
        return input_word, input_translation


