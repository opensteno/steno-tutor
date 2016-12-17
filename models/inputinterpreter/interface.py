# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""InputInterpreters translate plover's translation further."""


class InputInterpreter(object):

    """Catch the steno/translation plover provides and alter it if desired."""

    def run(self, input_word, word_to_type, 
            current_input_word, input_translation):
        
        """
        Retranslate user input word in case this should not be exactly what
        plover returned.
        
        @param input_word: steno word user has entered
        @param word_to_type: steno word user was presented with to type
        @param current_input_word: what the user had typed previously
                                   (the first part of a multistroke steno word,
                                   maybe)
        @param input_translation: translation of input_word (english)

        @type input_word: str
        @type word_to_type: str
        @type current_input_word: str
        @type input_translation: str

        @return: tuple (translated user input word in steno, input translation)
        @rtype: (str, str)
        """
        
        pass

