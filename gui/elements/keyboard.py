# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Onscreen keyboard showing where steno/qwerty keys are and which to press."""

from fly.gui import constants as c
from fly.gui import genericelements as gel
from fly.gui import helpers as guihelpers
from fly.gui.elements import interface
from fly.data import stenoqwerty
from fly import config


class Tinter(object):

    """Tints letters steno colors for easier comprehension."""

    # Ordered as per steno grid showing coloring for letters.
    TINT_MAP = {
        'S': (0, 255, 0),
        'T': (127, 0, 253), 
        'P': (0, 127, 255), 
        'R': (0, 254, 129),
        'B': (128, 0, 0),
        'D': (127, 129, 0),
        'F': (0, 128, 1),
        'G': (0, 128, 131),
        'J': (1, 0, 128),
        'K': (129, 0, 127),
        'L': (127, 255, 254),
        'M': (132, 63, 0),
        'N': (255, 0, 134),
        'V': c.V_KEY_STENO_COLOR,
        'X': (255, 255, 0),
        'Z': (255, 0, 0),
        'A': (157, 243, 72),
        'E': (238, 167, 51),
        'H': (197, 89, 211),
        'O': (71, 87, 113),
        'U': (188, 243, 237),
        'W': (242, 106, 191),
        'C': (176, 52, 50),
        'I': (88, 89, 21),
        'Q': (82, 15, 82),
        'Y': (115, 44, 174),
        '*': (100, 100, 100)}

    @classmethod
    def get_tint_on_letters(cls, qwerty_letter_list):

        """Get the color each qwerty letter should be tinted.

        @param qwerty_letter_list: list of keyboard letters for qwerty keyboard
        @type qwerty_letter_list: list of str

        @return: dict of qwerty letter to color it should be
        @rtype: dict of str to color (tuple (int, int, int) representing red,
                green, blue where each is between 0 and 255)
        """

        tint_map = {}
        qwerty_keys = ''.join(qwerty_letter_list)
        qwerty_key_groups = []
        for qwerty_combo_tuple in stenoqwerty.QWERTY_COMBO_STENO_LETTERS:
            qwerty_chars = set(qwerty_combo_tuple[0])
            if qwerty_chars.issubset(qwerty_keys):
                matched_letters = list(qwerty_chars.intersection(qwerty_keys))
                qwerty_keys = [k for k in qwerty_keys if k not in matched_letters]
                qwerty_key_groups.append(qwerty_combo_tuple)

        for leftover_key in qwerty_keys:
            steno_letter = stenoqwerty.QWERTY_TO_STENO_KEYS[leftover_key]
            tint_key = steno_letter.strip('-')
            qwerty_key_groups.append((leftover_key, tint_key))

        for letters in qwerty_letter_list:
            for letter in letters:
                for key_group, tint_key in qwerty_key_groups:
                    if letter in key_group:
                        tint = Tinter.TINT_MAP[tint_key]
                        tint_map[letter] = tint

        return tint_map


class KeyboardGUI(interface.GUIElementInterface):

    """Creates the image of a keyboard on screen, with qwerty/steno letters.
    Whether steno and/or qwerty letters are displayed on the keyboard can be
    configured in-game.
    
    The keys that the user must type to complete a word are more brightly lit
    than the surrounding keys.
    """

    def __init__(self):
        self.keys = []
        self.previous_keys_pressed = []
        self.display_steno_color = config.DISPLAY_STENO_COLOR
        self.has_key_highlighting = config.DISPLAY_KEY_HIGHLIGHTING
        self.__create_keyboard()

    def __create_keyboard(self):

        """Generate keyboard, where a keyboard is a collection of keys."""

        top_row_x_start = guihelpers.centred_for_x(c.TOP_ROW_LENGTH)
        yPos = c.TOP_ROW_Y
        self.__add_keys_in_row(top_row_x_start, c.TOP_ROW_Y, c.TOP_ROW)

        middle_row_x_start = top_row_x_start + c.MIDDLE_ROW_X_OFFSET_FROM_TOP
        yPos = c.TOP_ROW_Y + c.KEY_HEIGHT + c.KEY_Y_OFFSET
        self.__add_keys_in_row(middle_row_x_start, yPos, c.MIDDLE_ROW)

        xPos = middle_row_x_start + c.BOTTOM_ROW_X_OFFSET_FROM_MIDDLE
        yPos = yPos + c.KEY_HEIGHT + c.KEY_Y_OFFSET
        self.__add_keys_in_row(xPos, yPos, c.BOTTOM_ROW)

    def __add_keys_in_row(self, xStart, yStart, row):

        """Populate list of keys with row such as qwerty... or asdfg...

        @param xStart: x coordinate on screen for first key in row
        @param yStart: y coordinate on screen for first key in row
        @param row: list of keys in row, e.g. ["Q", "W", "E", "R" ...]
        
        @type xStart: int
        @type yStart: int
        @type row: list of str
        """

        xPos = xStart
        yPos = yStart
        for key in row:
            steno_key = ""
            if key in stenoqwerty.QWERTY_TO_STENO_KEYS:
                steno_key = stenoqwerty.QWERTY_TO_STENO_KEYS[key]
            key = gel.KeyboardKey((xPos, yPos), 
                             (c.KEY_WIDTH, c.KEY_HEIGHT), 
                             key,
                             steno_key)
            xPos += c.KEY_WIDTH
            xPos += c.KEY_X_OFFSET
            self.keys.append(key)

    def toggle_qwerty_display(self):

        """Toggle the display of qwerty keys overlaid on the keyboard."""

        for key in self.keys:    
            key.toggle_qwerty_display()
    
    def toggle_steno_display(self):

        """Toggle the display of steno keys overlaid on the keyboard."""

        for key in self.keys:
            key.toggle_steno_display()

    def toggle_steno_color(self):

        """Toggle tinting of keys to steno colors for letter associations."""

        self.display_steno_color = not self.display_steno_color

    def toggle_highlight_keys(self):

        """Toggles display of keys user must press to type word."""
        
        self.has_key_highlighting = not self.has_key_highlighting
        for key in self.keys:
            key.toggle_highlight()

    def was_hint_key_pressed(self):

        """Check if the hint key (left shift) was pressed.
        
        @return: whether hint key was pressed
        @rtype: bool
        """
        toggle_hint = False
        for key in self.keys:
            if key.toggle_hint:
                toggle_hint = True
                key.toggle_hint = False
        return toggle_hint

    def set_key_highlighting(self, value):

        """Set key highlighting to value.
        
        @param value: whether or not key highlighting should be used
        @type value: bool
        """

        for key in self.keys:
            key.highlight_keys = value
            self.has_key_highlighting = value
    
    def set_key_steno_text_visible(self, value):

        """Set visibility of steno label on keys to value.
        
        @param value: whether or not steno key text should be used
        @type value: bool
        """

        for key in self.keys:
            key.display_steno = value

    def on_key_down(self, event):

        """Called when keys on real keyboard are pressed. 
        Tell the image of the keyboard which keys have been pressed.
        
        @param event: key down event
        @type event: pygame.event
        """

        for key in self.keys:
            key.set_pressed(event.key)
            self.previous_keys_pressed.append(key)
        
    def show_word_to_type(self, qwerty_letter_list):

        """Highlight keys on the keyboard to indicate they should be pressed.
        
        @param qwerty_letter_list: list of letters to highlight. Each entry in 
                                   the list will usually contain only one 
                                   letter, however may contain two or more if
                                   a qwerty key corresponds to more than one 
                                   steno key (e.g. Q and A are steno S).
                                   
        @type qwerty_letter_list: list of str
        """

        self.clear_word_to_type()

        tint_map = Tinter.get_tint_on_letters(qwerty_letter_list)
        for qwerty_letters in qwerty_letter_list:
            if len(qwerty_letters) == 1:
                q_letter = qwerty_letters[0]
                # Highlight keys that need to be pressed.
                self.__set_keyboard_keys_lit(q_letter, tint_map, full_lit=True)
            else:
                for q_letter in qwerty_letters:
                    # Only one of these keys needs to be pressed. 
                    # Indicate by showing dimmed.
                    self.__set_keyboard_keys_lit(q_letter, 
                                                 tint_map, 
                                                 full_lit=False)
   
    def __set_keyboard_keys_lit(self, q_letter, tint_map, full_lit=True):
        
        """For the letter provided, highlight on the onscreen keyboard.
        If the letter is fully lit, this indicates it must be pressed. If it
        is partially lit, there will be other letters that are partially lit, 
        and only one of the partially lit letters needs to be pressed.

        Also, tint the letter a color to indicate the steno key belongs to a 
        qwerty letter.

        @param q_letter: qwerty letter to highlight
        @param tint_map: dict of qwerty letter to color it should be
        @param full_lit: whether it should be fully lit or partially lit

        @type q_letter: str
        @type tint_map: dict of str to color (tuple (int, int, int) 
                        representing red, green, blue where each is between 0 
                        and 255)
        @type full_lit: bool
        """

        for key in self.keys:

            if not self.display_steno_color:
                key.steno_tint_color = None

            if key.caption == q_letter:
                if full_lit:
                    key.lit = True
                else:
                    key.partial_lit = True
                
                if self.display_steno_color:
                    key.steno_tint_color = tint_map[q_letter]
                else:
                    key.steno_tint_color = None

    def clear_word_to_type(self):
        
        """Clear highlighted keys, so no keys are highlighted."""

        for key in self.keys:
            key.lit = False
            key.partial_lit = False
            key.steno_tint_color = None
        
    def reset(self):

        """Return to initial state with no keys pressed."""

        for key in self.previous_keys_pressed:
            key.pressed = False
            self.previous_keys_pressed.remove(key)

    def draw(self, surface):

        """Draw keyboard on screen."""

        for key in self.keys:
            key.blit_on(surface)


