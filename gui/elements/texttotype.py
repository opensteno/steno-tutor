# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Provides onscreen the text the user must type, both steno and english."""

from fly import config
from fly.gui import constants as c
from fly.gui import genericelements as gel
from fly.gui import helpers as guihelpers
from fly.gui.elements import interface


class TextToTypeGUI(interface.GUIElementInterface):

    """
    Display on screen the text the user must type to get the next word.
    The steno chord is displayed as well as the translation e.g. "S" and "is"
    """
    
    def __init__(self):
        # If word_style, display is two columns, otherwise one (sentence style)
        self.word_style = config.WORD_STYLE

        self.word_captions = []
        self.__add_word_to_type()
        self.__add_translation_to_type()

        self.sentence_captions = []
        self.__add_sentence_to_type()

    def __add_word_to_type(self):

        """Display steno chords on screen for user to type."""
    
        # Label for what this is. It's the chord (steno) word to type. 
        self.word_info_caption = \
                gel.Caption((guihelpers.centred_for_half_x(c.WORD_WIDTH), 
                             c.WORD_Y), c.CAPTION_FONT_SIZE, c.CAPTION_SIZE,
                             "Chord to Type:")
        self.word_captions.append(self.word_info_caption)

        # Word to type (steno)
        self.word_caption = \
                gel.Caption((guihelpers.centred_for_half_x(c.WORD_WIDTH), 
                             c.WORD_Y), 
                            c.WORD_FONT_SIZE, 
                            (c.WORD_WIDTH, c.WORD_HEIGHT), 
                            "", 
                            c.WORD_MARGIN, 
                            c.WORD_TEXT_COLOR, 
                            c.WORD_BACKGROUND_COLOR)

        # Don't necessarily display the steno chord to type--harder if it's
        # not displayed!
        self.word_caption.display_text = config.DISPLAY_INPUT_CHORD
        self.word_captions.append(self.word_caption)

    def __add_translation_to_type(self):

        """Display english translation on screen for user to type."""

        # Label for what this is. It's the english for the word to type.
        x_pos = guihelpers.centred_for_half_x(c.WORD_WIDTH, 
                                              left_screen_half=False)
        self.translation_info_caption = \
                gel.Caption((x_pos, c.WORD_Y), 
                            c.CAPTION_FONT_SIZE, 
                            c.CAPTION_SIZE, 
                            "Translation of Chord:")

        self.word_captions.append(self.translation_info_caption)

        # Word to type (translation english)
        x_pos = guihelpers.centred_for_half_x(c.WORD_WIDTH, 
                                              left_screen_half=False)
        self.translation_caption = gel.Caption((x_pos, c.WORD_Y), 
                                                c.WORD_FONT_SIZE, 
                                                (c.WORD_WIDTH, c.WORD_HEIGHT), 
                                                "", 
                                                c.WORD_MARGIN, 
                                                c.WORD_TEXT_COLOR, 
                                                c.WORD_BACKGROUND_COLOR)
        self.word_captions.append(self.translation_caption)

    def __add_sentence_to_type(self):

        """Display steno and english in a double length bar.
        This will never be displayed unless word_style is false. If that's 
        so, the word and translation captions set up previously will be 
        hidden.
        """

        element_width = 2*c.WORD_WIDTH + 2*c.WORD_MARGIN
        caption_size = (c.CAPTION_SIZE[0]*2 + 2*c.WORD_MARGIN, 
                        c.CAPTION_SIZE[1])

        # Label the input sentence bar, AND display chord to type (if user
        # wants)
        pos = (guihelpers.centred_for_x(element_width), c.WORD_Y)
        self.sentence_info_caption = gel.Caption(pos, 
                                                 c.CAPTION_FONT_SIZE, 
                                                 caption_size, 
                                                 "")
        self.sentence_info_caption.display_text = config.DISPLAY_INPUT_CHORD
        self.sentence_captions.append(self.sentence_info_caption)

        # Display sentence to type (translation)
        pos = (guihelpers.centred_for_x(element_width), c.WORD_Y)
        self.sentence_caption = gel.Caption(pos, 
                                            c.WORD_FONT_SIZE, 
                                            (element_width, c.WORD_HEIGHT), 
                                            "", 
                                            c.WORD_MARGIN, 
                                            c.WORD_TEXT_COLOR, 
                                            c.WORD_BACKGROUND_COLOR)
        self.sentence_captions.append(self.sentence_caption)

    def toggle_chord_to_type_display(self):

        """Toggle display of steno chord to type."""

        self.word_caption.display_text = (not self.word_caption.display_text)
        self.sentence_info_caption.display_text = \
                (not self.sentence_info_caption.display_text)

    def set_chord_to_type_display(self, value):

        """Set display of steno chord to type to value.
        
        @param value: whether to display chord to type
        @type value: bool
        """

        self.word_caption.display_text = value
        self.sentence_info_caption.display_text = value

    def toggle_style(self):

        """Toggle display style between one long bar and two shorter bars"""

        self.word_style = not self.word_style        

    def set_word(self, word):

        """Set steno chord to type.

        @param word: steno chord user must input
        @type word: str
        """

        if self.word_style:
            self.word_caption.set_text(word)
        else:
            self.sentence_info_caption.set_text("Words to type: "
                                                "(chord %s)" % word)

    def set_translation(self, translation):

        """Set english translation to type.

        @param translation: english word user must input
        @type translation: str
        """

        if self.word_style:
            self.translation_caption.set_text(translation)
        else:
            self.sentence_caption.set_text(translation)

    def draw(self, surface):

        """Display word to type on screen."""

        if self.word_style:
            for caption in self.word_captions:
                caption.blit_on(surface)
        else:
            for caption in self.sentence_captions:
                caption.blit_on(surface)


