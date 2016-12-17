# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Word choosers decide which words will be presented to user."""


class WordChooserInterface(object):

    """Interface for specifying how a word is chosen for the user to type."""
    
    def get_word_and_translation(self, level):

        """Return a chord and the corresponding translation of the chord.
        
        @param level: levels are numbered 1 to 6, where 6 is the hardest.
        @type level: int
        """

        raise NotImplementedError("Child classes must implement this method")

    def get_display_word_and_translation(self, level):

        """Get word and translation to be displayed in GUI.

        Optional. By default the display will not be any different from the 
        internal word/translation, but this can be overridden by word choosers
        if they need different behaviour.
        
        @param level: levels are numbered 1 to 6, where 6 is the hardest.
        @type level: int
        """

        pass

    def set_level(self, level):

        """Set the level of difficulty the user should be presented with.

        Optional. Doesn't have to apply to word chooser.

        @param level: levels are numbered 1 to 6, where 6 is the hardest.
        @type level: int
        """

        pass

    def return_inputs(self, input_word, input_translation):

        """Return the input word and translation.

        Optional. When retrieving the input word and translation from the 
        model, the word chooser can optionally modify it in case it should 
        display differently to what is actually there.

        @param input_word: word that user has input, run through input
                           interpreter.
        @param input_translation: translation of input word.

        @type input_word: str
        @type input_translation: str
        """

        return input_word, input_translation

    
