# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Model the game: what to present to the user, and how to interpret inputs."""

from fly.models import interface
from fly.models import keyhighlighting


class GameModel(interface.InteractionModelInterface):

    """Game model, configurable to allow different modes of operation."""

    # Determines which keys are lit to indicate keys user is to press.
    key_highlighter = keyhighlighting.KeyHighlighter()

    def __init__(self, name, word_chooser, input_interpreter):

        """
        @param word_chooser: what will be used to determine word to present
                             to user as what they should type.
        @param input_interpreter: what will be used to interpret user input.

        @type new_word_chooser: L{models.wordchooser.interface.
                                  WordChooserInterface}
        @type input_interpreter: L{models.inputinterpreter.
                                   interface.InputInterpreter}
        """

        self.name = name
        self.word_chooser = word_chooser
        self.input_interpreter = input_interpreter

        self.word = ""
        self.translation = ""
        self.previous_word = ""
        self.input_word = ""
        self.input_translation = ""
        self.current_level = 1

    def switch_level(self, level):

        """Set level of difficulty in choosing words to present.

        @param level: levels are numbered 1 to 6, where 6 is the hardest.
        @type level: int
        """

        if self.current_level != level:
            self.word_chooser.set_level(level)
            self.current_level = level

    def set_word_chooser(self, new_word_chooser):

        """Change word chooser to new_word_chooser.

        @param new_word_chooser: the word chooser to switch to.
        @type new_word_chooser: L{models.interface.WordChooserInterface}
        """

        self.word_chooser = new_word_chooser

    def generate_word_to_type(self): 

        """Get a new word and translation, set on model for user to type."""

        self.word, self.translation = \
                self.word_chooser.get_word_and_translation(self.current_level)

    def get_display_word_and_translation(self):

        """Provide word user must type to progress, and translation.

        This is for the GUI only.

        @return: tuple of (word to type, translation of word)
        @rtype: (str, str)
        """

        level = self.current_level
        result = self.word_chooser.get_display_word_and_translation(level)
        
        # Not forcing the word chooser to implement 
        # get_display_word_and_translation. If None is returned, not 
        # implemented, so use results generating word to type.
        if result is None:
            return self.word, self.translation

        return result[0], result[1]

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

        results = self.input_interpreter.run(word, self.word, 
                                             self.input_word, translation)
        input_word = results[0]
        input_translation = results[1]

        if input_word:
            self.input_word = input_word
        if input_translation:
            self.input_translation = input_translation

    def get_chord_and_translation(self):

        """return word user entered, and translation of that word.

        @return: tuple of (input_word, input_translation)
        @rtype: (str, str)
        """

        # Run inputs through word chooser in case the display should
        # not be the actual input word/translation.
        return self.word_chooser.return_inputs(self.input_word, 
                                               self.input_translation)
    
    def right_word_entered(self):

        """Determine whether right word has been entered.

        @return: whether right word has been entered.
        @rtype: bool
        """

        if self.translation.lower() == self.input_translation.lower() or \
           self.word.lower() == self.input_word.lower():
            return True
        return False
    
    def clear_inputs(self):

        """Blank input word and translation."""

        self.input_word = ""
        self.input_translation = ""
    
    def wrong_word_entered(self):

        """Find out whether the word entered is incorrect.
        
        This is called when the right word hasn't been entered.
        It checks whether a word has been completed. If it has, the
        word is incorrect.

        @return: whether word is incorrect.
        @rtype: bool
        """

        len_input = len(self.input_word.lstrip("-"))
        len_word = len(self.word.lstrip("-"))
        if len_input >= len_word and not self.input_word == self.previous_word:
            self.previous_word = self.input_word
            return True
        return False

    def get_qwerty_letters_to_type(self):

        """Get a list of the qwerty letters that should be pressed next.
       
        @return: list of letters, some of which will have multiple letters
                 e.g. ['QA', 'R']
        @rtype: list of str
        """

        return self.key_highlighter.get_qwerty_letters_to_type(self.word, 
                                                               self.input_word)


