# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Right-most panel in the game, displaying options that the user can click."""

from fly.gui.elements import interface
from fly.gui import constants as c
from fly.gui import genericelements as gel
from fly.models import threemode
from fly import config


class OptionsPanelGUI(interface.GUIElementInterface):

    """Right-most options panel, providing options for user to click.
    The panel is split into the top part (GameOptionsPanel) and the
    bottom (DisplayOptionsPanel). 
    """

    def __init__(self, keyboard, text_to_type, text_input, 
                 info_panel, speed_bar, lesson_names):

        """
        @param keyboard: Keyboard GUIElement object
        @param text_to_type: TextToType GUIElement object
        @param text_input: TextInput GUIElement object
        @param info_panel: InfoPanel GUIElement object
        @param speed_bar: SpeedBar GUIElement object
        @param lesson_names: list of names of lessons

        @type keyboard: L{KeyboardGUI}
        @type text_to_type: L{TextToTypeGUI}
        @type text_input: L{TextInputGUI}
        @type info_panel: L{InfoPanelGUI}
        @type speed_bar: L{SpeedBarGUI}
        @type lesson_names: list of str
        """

        self.game_options_panel = GameOptionsPanelGUI(info_panel, lesson_names)
        self.display_options_panel = \
                DisplayOptionsPanelGUI(keyboard, text_to_type, text_input, 
                                       info_panel, speed_bar)
    
        # Create box with "GAME OPTIONS" text
        x_pos = c.SCREEN_WIDTH - c.MENU_BAR_WIDTH
        self.menu_bar = gel.DisplayPanel((x_pos, 0), 
                                        (c.MENU_BAR_WIDTH, c.SCREEN_HEIGHT), 
                                        "GAME OPTIONS", 
                                        c.MENU_BAR_COLOR, 
                                        c.MENU_BAR_TEXT_COLOR)

        # Create text label for display options at bottom
        self.display_option_caption = gel.Caption((c.OPTION_DISPLAY_CAPTION_X, 
                                                   c.OPTION_DISPLAY_CAPTION_Y),
                                                   16, 
                                                   c.CAPTION_SIZE,
                                                   "DISPLAY OPTIONS", 
                                                   text_color=c.MENU_BAR_TEXT_COLOR, 
                                                   background_color=c.MENU_BAR_COLOR)

    def get_mode(self):

        """Return the mode the game is operating in, e.g. alphabet.

        @return: game mode (model)
        @rtype: str
        """
        
        return self.game_options_panel.mode
    
    def get_current_lesson_name(self):

        """@rtype: str"""

        return self.game_options_panel.current_lesson_name

    def on_mouse_motion(self, event):

        """Tell game and display options panel about event."""

        self.game_options_panel.on_mouse_motion(event)
        self.display_options_panel.on_mouse_motion(event)

    def on_right_mouse_down(self, event):

        """Tell game and display options panel about event."""

        self.game_options_panel.on_right_mouse_down(event)
        self.display_options_panel.on_right_mouse_down(event)

    def on_right_mouse_up(self, event):

        """Tell game and display options panel about event."""

        self.game_options_panel.on_right_mouse_up(event)
        self.display_options_panel.on_right_mouse_up(event)

    def act_on_hint_key_press(self):

        """Pass through act_on_hint_key_press signal."""

        self.display_options_panel.act_on_hint_key_press()
    
    def draw(self, surface):

        """Draw captions for both panels and display them."""

        self.menu_bar.blit_on(surface)
        self.display_option_caption.blit_on(surface)
        
        self.game_options_panel.draw(surface)
        self.display_options_panel.draw(surface)


class GameOptionsPanelGUI(interface.GUIElementInterface):

    """
    Allows the user to select which game model they wish to use.
    If in lesson mode, also allow the choice of lessons.
    """

    ALPHABET_MODE = threemode.ALPHABET_MODEL_NAME
    WORD_MODE = threemode.WORD_MODEL_NAME
    LESSON_MODE = threemode.LESSON_MODEL_NAME

    def __init__(self, info_panel, lesson_names):

        """
        @param info_panel: InfoPanel GUIElement object
        @param lesson_names: list of names of lessons

        @type info_panel: L{InfoPanelGUI}
        @type lesson_names: list of str
        """

        self.info_panel = info_panel
        self.buttons = []

        self.mode = self.ALPHABET_MODE
       
        self.lesson_names = lesson_names
        self.lesson_index = 0
        self.current_lesson_name = self.lesson_names[self.lesson_index]

        self.__add_alphabet_button()
        self.__add_word_button()        
        self.__add_lesson_button()
        self.__add_lesson_chooser_button()

    def __add_alphabet_button(self):

        """Add button which, when pressed, activates alphabet mode."""

        self.alphabet_mode_button, self.alphabet_mode_help_button = \
                self.__get_button_and_sub_button(1, "Alphabet Mode")
        self.alphabet_mode_button.onclick = self.__alphabet_mode_set
        self.alphabet_mode_help_button.onclick = \
                self.__display_alphabet_mode_info
        self.alphabet_mode_button.set_active(True)
        self.buttons.append(self.alphabet_mode_button)
        self.buttons.append(self.alphabet_mode_help_button)

    def __alphabet_mode_set(self):

        """Called when alphabet mode button is clicked on."""

        self.alphabet_mode_button.set_active(True)
        self.word_mode_button.set_active(False)
        self.lesson_mode_button.set_active(False)
        self.mode = self.ALPHABET_MODE

    def __display_alphabet_mode_info(self):

        """Called when the '?' next to the alphabet button is clicked."""

        self.info_panel.set_info(c.ALPHABET_INFO_TEXT)

    def __add_word_button(self):

        """Add button which, when pressed, activates word mode."""

        self.word_mode_button, self.word_mode_help_button = \
                self.__get_button_and_sub_button(2, "Word Mode")
        self.word_mode_button.onclick = self.__word_mode_set
        self.word_mode_help_button.onclick = self.__display_word_mode_info
        self.buttons.append(self.word_mode_button)
        self.buttons.append(self.word_mode_help_button)

    def __word_mode_set(self):

        """Called when word mode button is clicked on."""

        self.alphabet_mode_button.set_active(False)
        self.word_mode_button.set_active(True)
        self.lesson_mode_button.set_active(False)
        self.mode = self.WORD_MODE

    def __display_word_mode_info(self):

        """Called when the '?' next to the word button is clicked."""

        self.info_panel.set_info(c.WORD_INFO_TEXT)

    def __add_lesson_button(self):

        """Add button which, when pressed, activates lesson mode."""

        self.lesson_mode_button, self.lesson_mode_help_button = \
                self.__get_button_and_sub_button(3, "Lesson Mode")
        self.lesson_mode_button.onclick = self.__lesson_mode_set
        self.lesson_mode_help_button.onclick = self.__display_lesson_mode_info
        self.buttons.append(self.lesson_mode_button)
        self.buttons.append(self.lesson_mode_help_button)

    def __lesson_mode_set(self):
        
        """Called when lesson mode button is clicked on."""

        self.alphabet_mode_button.set_active(False)
        self.word_mode_button.set_active(False)
        self.lesson_mode_button.set_active(True)

        # When lesson mode is activated, display the current lesson
        # with an option to advance to the next (">")
        self.lesson_name_button.display = True
        self.lesson_advance_button.display = True
        self.mode = self.LESSON_MODE
    
    def __display_lesson_mode_info(self):

        """Called when the '?' next to the lesson button is clicked."""

        self.info_panel.set_info(c.LESSON_INFO_TEXT)

    def __add_lesson_chooser_button(self):

        """Add 'go right' button to switch to the next lesson in the list."""

        buttons = self.__get_button_and_sub_button(4, 
                                                   self.current_lesson_name, 
                                                   ">", 
                                                   indent=True)
        self.lesson_name_button = buttons[0]
        self.lesson_name_button.hover_color = self.lesson_name_button.color
        self.lesson_name_button.pressed_color = self.lesson_name_button.color
        self.lesson_name_button.display = False

        self.lesson_advance_button = buttons[1]
        self.lesson_advance_button.display = False
        self.lesson_advance_button.onclick = self.__display_next_lesson_name

        self.buttons.append(self.lesson_name_button)
        self.buttons.append(self.lesson_advance_button)

    def __display_next_lesson_name(self):

        """When '>' is clicked, the next lesson name is displayed."""

        self.lesson_index += 1
        if self.lesson_index >= len(self.lesson_names):
            self.lesson_index = 0
        self.current_lesson_name = self.lesson_names[self.lesson_index]
        self.lesson_name_button.set_text(self.current_lesson_name)
    
    def __get_button_and_sub_button(self, display_slot, caption, 
                                    sub_button_caption="?", indent=False):

        """Create a main button and a 1-char wide button to the right.
        The second button is for help on the main button or similar.

        @param display_slot: the position at which to create the button, where
                             1 is at the top of the option panel, 2 is next
                             row, and so on.
        @param caption: label for the main button
        @param sub_button_caption: label for the sub button
        @param indent: whether the main button should be indented to indicate
                       it is a child of the button in the display slot above.

        @type display_slot: int
        @type caption: str
        @type sub_button_caption: str
        @type indent: bool
        """

        x_position = c.OPTION_BUTTON_X_POS
        width = c.OPTION_BUTTON_WITH_HELP_WIDTH
        if indent:
            x_position += 20
            width -= 20

        y_position = display_slot*c.OPTION_MARGIN + c.OPTION_START_Y + \
                (display_slot-1)*c.OPTION_HEIGHT

        button = gel.Button((x_position, y_position), 
                            (width, c.OPTION_HEIGHT),
                            caption = caption, 
                            color = c.OPTION_BACKGROUND_COLOR, 
                            text_color = c.OPTION_TEXT_COLOR)

        y_position_help = display_slot*c.OPTION_MARGIN + c.OPTION_START_Y + \
                (display_slot-1)*c.OPTION_HEIGHT

        help_button = gel.Button((c.OPTION_BUTTON_HELP_X_POS,
                                 y_position_help), 
                                 (c.OPTION_BUTTON_HELP_WIDTH, c.OPTION_HEIGHT),
                                 caption = sub_button_caption, 
                                 color = c.OPTION_BACKGROUND_COLOR, 
                                 text_color = c.OPTION_TEXT_COLOR)

        return (button, help_button)

    def on_mouse_motion(self, event):

        """Tell game and display options panel about event."""

        for button in self.buttons:
            if button.contains(event.pos): 
                button.hover = True
            else: 
                button.hover = False
                button.pressed = False

    def on_right_mouse_down(self, event):

        """Tell game and display options panel about event."""

        for button in self.buttons:
            if button.contains(event.pos): 
                button.pressed = True

    def on_right_mouse_up(self, event):

        """Tell game and display options panel about event."""

        for button in self.buttons:
            if button.pressed and button.onclick != None: 
                button.onclick()
            button.pressed = False
    
    def draw(self, surface):

        """Draw game options panel on screen."""

        for button in self.buttons:
            button.blit_on(surface)


class DisplayOptionsPanelGUI(interface.GUIElementInterface):

    def __init__(self, keyboard, text_to_type, 
                 text_input, info_panel, speed_bar):

        """
        @param keyboard: Keyboard GUIElement object
        @param text_to_type: TextToType GUIElement object
        @param text_input: TextInput GUIElement object
        @param info_panel: InfoPanel GUIElement object
        @param speed_bar: SpeedBar GUIElement object

        @type keyboard: L{KeyboardGUI}
        @type text_to_type: L{TextToTypeGUI}
        @type text_input: L{TextInputGUI}
        @type info_panel: L{InfoPanelGUI}
        @type speed_bar: L{SpeedBarGUI}
        """

        self.keyboard = keyboard
        self.text_to_type = text_to_type
        self.text_input = text_input
        self.info_panel = info_panel
        self.speed_bar = speed_bar
        self.hints_on = True
        self.buttons = []

        self.__add_display_qwerty_button()
        self.__add_display_steno_button()
        self.__add_display_chord_to_type_button()
        self.__add_highlight_keys_button()
        self.__add_info_button()
        self.__add_display_speed_bar_button()
        self.__add_toggle_word_sentence_button()
        self.__add_toggle_steno_color_button()

    def __add_display_qwerty_button(self):

        """Add button to toggle the visibility of qwerty keys on keyboard."""

        self.qwerty_option_button = \
                self.__get_button(1, "Toggle QWERTY Display")
        self.qwerty_option_button.onclick = self.__toggle_qwerty_clicked
        self.buttons.append(self.qwerty_option_button)

    def __toggle_qwerty_clicked(self):

        """'Toggle QWERTY Display' button clicked; do it."""

        self.keyboard.toggle_qwerty_display()

    def __add_display_steno_button(self):

        """Add button to toggle the visibility of steno keys on keyboard."""

        self.steno_option_button = self.__get_button(2, "Toggle Steno Display")
        self.steno_option_button.onclick = self.__toggle_steno_clicked
        self.buttons.append(self.steno_option_button)

    def __toggle_steno_clicked(self):

        """'Toggle Steno Display' button clicked; do it."""

        self.keyboard.toggle_steno_display()

    def __add_display_chord_to_type_button(self):

        """Add button to toggle the visibility of chord to type."""

        self.chord_to_type_option_button = \
                self.__get_button(3, "Toggle Input Chord Display")
        self.chord_to_type_option_button.onclick = \
                self.__toggle_chord_to_type_display_clicked
        self.buttons.append(self.chord_to_type_option_button)

    def __toggle_chord_to_type_display_clicked(self):
        
        """'Toggle Input Chord Display' button clicked; do it."""

        self.text_to_type.toggle_chord_to_type_display()

    def __add_highlight_keys_button(self):

        """Add button to toggle key highlighting for keys on screen."""

        self.highlight_keys_option_button = \
                self.__get_button(4, "Toggle Key Highlighting")
        self.highlight_keys_option_button.onclick = \
                self.__toggle_highlight_keys_clicked
        self.buttons.append(self.highlight_keys_option_button)

    def __toggle_highlight_keys_clicked(self):
        
        """'Toggle Key Highlighting' button clicked; do it."""

        self.keyboard.toggle_highlight_keys()
    
    def __add_info_button(self):
        
        """Add button to toggle display of info panel."""

        self.info_option_button = self.__get_button(5, "Toggle Info Display")
        self.info_option_button.onclick = self.__toggle_info
        self.buttons.append(self.info_option_button)

    def __toggle_info(self):

        """'Toggle Info Display' button clicked; do it."""

        self.info_panel.toggle_info_panel()

    def __add_display_speed_bar_button(self):
        
        """Add button to toggle display of speed bar."""

        self.display_speed_button = self.__get_button(6, "Toggle Speed Display")
        self.display_speed_button.onclick = self.__toggle_speed_display
        self.buttons.append(self.display_speed_button)

    def __toggle_speed_display(self):
        
        """'Toggle Speed Display' button clicked; do it."""

        self.speed_bar.toggle_display()

    def __add_toggle_word_sentence_button(self):
        self.word_sentence_button = self.__get_button(7, "Toggle Word/Sentence")
        self.word_sentence_button.onclick = self.__toggle_word_sentence
        self.buttons.append(self.word_sentence_button)

    def __toggle_word_sentence(self):
        
        """'Toggle Word/Sentence' button clicked; do it."""

        self.text_to_type.toggle_style()
        self.text_input.toggle_style()

    def __add_toggle_steno_color_button(self):
        self.steno_color_button = self.__get_button(8, "Toggle Steno Color")
        self.steno_color_button.onclick = self.__toggle_steno_color
        self.buttons.append(self.steno_color_button)

    def __toggle_steno_color(self):
        
        """'Toggle Steno Color' button clicked; do it."""

        self.keyboard.toggle_steno_color()

    def __get_button(self, display_slot, caption):

        """Create a button in a position from the bottom of the screen.
        
        @param display_slot: row button is on from bottom of screen (1 will be
                             lowest, 2 will be second lowest, and so on)
        @param caption: label for button

        @type display_slot: int
        @type caption: str
        """

        y_position = c.SCREEN_HEIGHT - c.OPTION_MARGIN - c.OPTION_HEIGHT - \
            (display_slot*c.OPTION_MARGIN + (display_slot-1)*c.OPTION_HEIGHT)
        return gel.Button((c.OPTION_BUTTON_X_POS,
                          y_position),
                          (c.OPTION_BUTTON_WIDTH, c.OPTION_HEIGHT),
                          caption = caption, 
                          color = c.OPTION_BACKGROUND_COLOR, 
                          text_color = c.OPTION_TEXT_COLOR)
    
    def on_mouse_motion(self, event):

        """Tell game and display options panel about event."""

        for button in self.buttons:
            if button.contains(event.pos): 
                button.hover = True
            else: 
                button.hover = False
                button.pressed = False

    def on_right_mouse_down(self, event):

        """Tell game and display options panel about event."""

        for button in self.buttons:
            if button.contains(event.pos): 
                button.pressed = True

    def on_right_mouse_up(self, event):

        """Tell game and display options panel about event."""

        for button in self.buttons:
            if button.pressed and button.onclick != None: 
                button.onclick()
            button.pressed = False

    def act_on_hint_key_press(self):

        """Check whether user has pressed hotkey (left shift).

        Pressing left shift disables or enables all hint options.
        """

        if not self.keyboard.was_hint_key_pressed():
            return

        # Use key highlighting as main hint that drives whether 
        # hints are on or off
        hint_options = config.HINT_OPTIONS
        if not hint_options:
            return

        hint_options = hint_options.lower()
        if self.hints_on:
            if hint_options.find("keyhighlighting") != -1:
                self.keyboard.set_key_highlighting(False)
            if hint_options.find("keystenotext") != -1:
                self.keyboard.set_key_steno_text_visible(False)
            if hint_options.find("chordtotypedisplay") != -1:
                self.text_to_type.set_chord_to_type_display(False)
            self.hints_on = False
        else:
            if hint_options.find("keyhighlighting") != -1:
                self.keyboard.set_key_highlighting(True)
            if hint_options.find("keystenotext") != -1:
                self.keyboard.set_key_steno_text_visible(True)
            if hint_options.find("chordtotypedisplay") != -1:
                self.text_to_type.set_chord_to_type_display(True)
            self.hints_on = True

    def draw(self, surface):

        """Draw display options panel on screen."""

        for button in self.buttons:
            button.blit_on(surface)


