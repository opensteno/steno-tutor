# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""For displaying user input on screen, steno chords and translation."""

from fly import config
from fly.gui import constants as c
from fly.gui import genericelements as gel
from fly.gui import helpers as guihelpers
from fly.gui.elements import interface


class TextInputGUI(interface.GUIElementInterface):

    """Display on screen what the user has typed."""

    def __init__(self):
        self.word_captions = []
        self.__add_text_input()
        self.__add_input_translation()
        self.word_style = config.WORD_STYLE

        self.sentence_captions = []
        self.__add_sentence_input()

    def __add_text_input(self):
        
        """Display what the user has typed in steno chords."""
        
        # Describe what the box represents with a caption
        pos_x = guihelpers.centred_for_half_x(c.TEXT_INPUT_WIDTH)
        self.info_caption = gel.Caption((pos_x, c.TEXT_INPUT_Y), 
                                        c.CAPTION_FONT_SIZE, 
                                        c.CAPTION_SIZE, 
                                        "Input Chord:")

        # Add box with user input in steno
        pos_x = guihelpers.centred_for_half_x(c.TEXT_INPUT_WIDTH)
        self.input_word = gel.Caption((pos_x, c.TEXT_INPUT_Y),
                                      c.TEXT_INPUT_FONT_SIZE, 
                                      (c.TEXT_INPUT_WIDTH, 
                                       c.TEXT_INPUT_HEIGHT),
                                      "",
                                      c.WORD_MARGIN,
                                      c.TEXT_INPUT_TEXT_COLOR,
                                      c.TEXT_INPUT_BACKGROUND_COLOR)
        self.word_captions.append(self.info_caption)
        self.word_captions.append(self.input_word)

    def __add_input_translation(self):

        """Display what the user has typed as translation (english)."""

        # Caption to describe what the box represents
        pos_x = guihelpers.centred_for_half_x(c.TEXT_INPUT_WIDTH, 
                                              left_screen_half=False)
        self.input_translation_caption = gel.Caption((pos_x, c.TEXT_INPUT_Y),
                                                     c.CAPTION_FONT_SIZE, 
                                                     c.CAPTION_SIZE, 
                                                     "Input Translation:")

        # Box with user input translation as text
        pos_x = guihelpers.centred_for_half_x(c.TEXT_INPUT_WIDTH, 
                                               left_screen_half=False)
        self.input_translation = gel.Caption((pos_x, c.TEXT_INPUT_Y),
                                             c.TEXT_INPUT_FONT_SIZE, 
                                             (c.TEXT_INPUT_WIDTH, 
                                              c.TEXT_INPUT_HEIGHT),
                                             "",
                                             c.WORD_MARGIN,
                                             c.TEXT_INPUT_TEXT_COLOR,
                                             c.TEXT_INPUT_BACKGROUND_COLOR)
        self.word_captions.append(self.input_translation_caption)
        self.word_captions.append(self.input_translation)

    def __add_sentence_input(self):

        """Alternate form of display with chord in label, translation in box."""

        element_width = 2*c.WORD_MARGIN + 2*c.TEXT_INPUT_WIDTH
        caption_size = (c.CAPTION_SIZE[0]*2 + 2*c.WORD_MARGIN, 
                        c.CAPTION_SIZE[1])

        # Label for sentence
        pos_x = guihelpers.centred_for_x(element_width)
        self.sentence_info_caption = gel.Caption((pos_x,
                                                 c.TEXT_INPUT_Y), 
                                                 c.CAPTION_FONT_SIZE, 
                                                 caption_size, 
                                                 "Input:")

        # Sentence
        pos_x = guihelpers.centred_for_x(element_width)
        self.input_sentence = gel.Caption((pos_x, c.TEXT_INPUT_Y),
                                          c.TEXT_INPUT_FONT_SIZE, 
                                          (element_width, c.TEXT_INPUT_HEIGHT),
                                          "", 
                                          c.WORD_MARGIN,
                                          c.TEXT_INPUT_TEXT_COLOR,
                                          c.TEXT_INPUT_BACKGROUND_COLOR)
        self.sentence_captions.append(self.sentence_info_caption)
        self.sentence_captions.append(self.input_sentence)

    def toggle_style(self):

        """Toggle between word style and sentence style.
        Word style has two boxes side by side for chord and translation whereas
        sentence style has the chord in the label and the translation in the
        box.
        """

        self.word_style = not self.word_style        

    def set_word_and_translation(self, chord, translation):

        """User has input word, set text of boxes.
        
        @param chord: steno word
        @param translation: english translation of chord
        
        @type chord: str
        @type translation: str
        """

        if chord is not "" and translation is not "":
            if self.word_style:
                self.input_word.set_text(chord)
                self.input_translation.set_text(translation)
            else:
                self.sentence_info_caption.set_text("Input (chord %s):" 
                                                    % chord)
                self.input_sentence.set_text(translation)

    def clear_words(self):

        """Reset to initial state, showing no user input."""

        self.input_word.set_text("")
        self.input_translation.set_text("")
        self.input_sentence.set_text("")
        self.sentence_info_caption.set_text("Input:")

    def draw(self, surface):

        """Draw GUI element on screen."""

        if self.word_style:
            for caption in self.word_captions:
                caption.blit_on(surface)
        else:
            for caption in self.sentence_captions:
                caption.blit_on(surface)


