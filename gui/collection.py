# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Collect all elements to display on screen."""

from fly.gui.elements import infopanel
from fly.gui.elements import keyboard
from fly.gui.elements import optionspanel
from fly.gui.elements import speedbar
from fly.gui.elements import textinput
from fly.gui.elements import texttotype


class ElementsCollection(object):

    """
    This is a collection of everything that is displayed on the screen, with 
    methods to interact with the elements. 
    """

    def __init__(self, lesson_names):

        """
        @param lesson_names: list of names of lessons to display in GUI.
        @type lesson_names: list of str
        """

        self.keyboard = keyboard.KeyboardGUI()
        self.text_to_type = texttotype.TextToTypeGUI()
        self.text_input = textinput.TextInputGUI()
        self.info_panel = infopanel.InfoPanelGUI()
        self.speed_bar = speedbar.SpeedBarGUI()
        self.options_panel = optionspanel.OptionsPanelGUI(self.keyboard, 
                                                          self.text_to_type, 
                                                          self.text_input, 
                                                          self.info_panel,
                                                          self.speed_bar,
                                                          lesson_names)
        self.gui_elements = [self.keyboard, self.text_to_type, 
                             self.text_input, self.options_panel,
                             self.info_panel, self.speed_bar]

    def draw(self, surface):

        """Paint element on screen.

        @param surface: screen to draw on.
        @type surface: pygame.Surface
        """

        for element in self.gui_elements:
            element.draw(surface)

    def on_mouse_motion(self, event):

        """React to mouse movement.

        @param event: mouse motion event
        @type event: pygame.event
        """

        for element in self.gui_elements:
            element.on_mouse_motion(event)

    def on_right_mouse_down(self, event):
        
        """React to right mouse button down event.

        @param event: mouse event
        @type event: pygame.event
        """

        for element in self.gui_elements:
            element.on_right_mouse_down(event)

    def on_right_mouse_up(self, event):
        
        """React to right mouse button up event.

        @param event: mouse event
        @type event: pygame.event
        """

        for element in self.gui_elements:
            element.on_right_mouse_up(event)

    def on_key_down(self, event):
        
        """React to a key press down from keyboard.

        @param event: key press event
        @type event: pygame.event
        """

        for element in self.gui_elements:
            element.on_key_down(event)

    def reset(self):
        
        """Restore elements to initial state."""

        for element in self.gui_elements:
            element.reset()

    def set_word_to_type(self, word, translation):

        """Present to user the word they should type.

        @param word: steno chords to type
        @param translation: english word to type

        @type word: str
        @type translation: str
        """

        self.text_to_type.set_word(word)
        self.text_to_type.set_translation(translation)
    
    def set_input_word_and_translation(self, word, translation):

        """Display word and translation provided by user on screen.

        @param word: steno chords user has typed
        @param translation: translation of what the user has typed

        @type word: str
        @type translation: str
        """

        self.text_input.set_word_and_translation(word, translation)

    def show_word_to_type(self, word):

        """Display word to type by highlighting keys on keyboard.

        @param word: steno chord user should type
        @type word: str
        """

        self.keyboard.show_word_to_type(word)

    def on_right_word_entered(self):

        """Called when correct word is entered."""

        self.keyboard.clear_word_to_type()
        self.text_input.clear_words()

    def update_speed_bar(self, words_per_minute, fractional_accuracy):

        """Update display of speed bar with new statistics.

        @param words_per_minute: number of words per minute user is typing
        @param fractional_accuracy: what fraction of words user is getting
                                    right, as a fraction between 0 and 1.

        @type words_per_minute: float
        @type fractional_accuracy: float
        """

        self.speed_bar.set_words_per_minute(words_per_minute)
        self.speed_bar.set_accuracy(fractional_accuracy)

    def toggle_text_field_style(self):

        """Toggle draw style of text field display and input. 

        This can stretch across screen, or be split in two to display
        chord and translation side by side.
        """

        self.text_to_type.toggle_style()
        self.text_input.toggle_style()

    def get_model_to_use(self):

        """
        @return: name of model currently selected in GUI.
        @rtype: str
        """

        return self.options_panel.get_mode()

    def get_current_lesson_name(self):

        """
        @return: lesson currently selected in GUI.
        @rtype: str
        """

        return self.options_panel.get_current_lesson_name()

    def act_on_hint_key_press(self):

        """Check if hint key (left shift) has been pressed, and toggle hints"""

        self.options_panel.act_on_hint_key_press()

