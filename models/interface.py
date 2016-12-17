# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Model for the operation of the game."""


class InteractionModelInterface(object):

    """Model for the game."""

    def switch_level(self, level):

        """Set level of difficulty in choosing words to present.

        @param level: levels are numbered 1 to 6, where 6 is the hardest.
        @type level: int
        """

        pass    
    
    def set_word_chooser(self, new_word_chooser):

        """Change word chooser to new_word_chooser.

        @param new_word_chooser: the word chooser to switch to.
        @type new_word_chooser: L{models.interface.WordChooserInterface}
        """

        pass        

    def generate_word_to_type(self):
        
        """Get a new word and translation, set on model for user to type.
        
        @return: (steno word, translation)
        @rtype: (str, str)
        """

        raise NotImplementedError("Child classes must implement this method!")

    def get_display_word_and_translation(self):

        """Provide word user must type to progress, and translation.

        This is for the GUI only.

        @return: tuple of (word to type, translation of word)
        @rtype: (str, str)
        """

        raise NotImplementedError("Child classes must implement this method!")

    def set_input_word_and_translation(self, word, translation):
        
        """User has entered word as given (with translation as provided).

        Run through input interpreter in case it shouldn't be set as 
        given. For example in the alphabet model, the translation shouldn't
        be used as it would be more useful to translate the word as steno
        alphabet letters.
        
        @param word: user entered chord, steno letters.
        @param translation: translation of user entered chord as according to
                            plover dictionary.

        @type word: str
        @type translation: str
        """

        pass

    def get_chord_and_translation(self):

        """return word user entered, and translation of that word.

        @return: tuple of (input_word, input_translation)
        @rtype: (str, str)
        """

        raise NotImplementedError("Child classes must implement this method!")

    def right_word_entered(self):
        
        """Determine whether right word has been entered.

        @return: whether right word has been entered.
        @rtype: bool
        """
        
        raise NotImplementedError("Child classes must implement this method!")

    def clear_inputs(self):
        
        """Blank input word and translation."""
        
        pass

    def wrong_word_entered(self):
        
        """Find out whether the word entered is incorrect.
        
        This is called when the right word hasn't been entered.
        It checks whether a word has been completed. If it has, the
        word is incorrect.

        @return: whether word is incorrect.
        @rtype: bool
        """
        
        raise NotImplementedError("Child classes must implement this method!")

    def get_qwerty_letters_to_type(self):
        
        """Get a list of the qwerty letters that should be pressed next.
       
        @return: list of letters, some of which will have multiple letters
                 e.g. ['QA', 'R']
        @rtype: list of str
        """

        raise NotImplementedError("Child classes must implement this method!")


