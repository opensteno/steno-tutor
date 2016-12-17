# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Constants such as resolution and size of elements"""

import logging
logger = logging.getLogger(__name__)

from fly import __version__
from fly import config

colour_scheme = config.COLOR_SCHEME
SUPPORTED_COLOR_SCHEMES = ["classic", "light", "highcontrast"]
if colour_scheme not in SUPPORTED_COLOR_SCHEMES:
    logger.error("Bad colour scheme found: %s. Must be one of "
                 "%s." % (colour_scheme, SUPPORTED_COLOR_SCHEMES))
    from fly.gui.color.classic import *
else:
    if colour_scheme == "highcontrast":
        from fly.gui.color.highcontrast import *
    elif colour_scheme == "light":
        from fly.gui.color.light import *
    else:
        from fly.gui.color.classic import *


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
MENU_BAR_WIDTH = 200

# Word field
WORD_WIDTH = 375
WORD_HEIGHT = 45
WORD_MARGIN = 10
WORD_Y = 10
WORD_FONT_SIZE = 45

# Text input field
TEXT_INPUT_WIDTH = WORD_WIDTH
TEXT_INPUT_HEIGHT = WORD_HEIGHT
TEXT_INPUT_FONT_SIZE = WORD_FONT_SIZE
TEXT_INPUT_Y = WORD_Y + 85

# Speed bar
SPEED_BAR_MAX_SPEED = 300  # Words per minute
SPEED_BAR_BLOCK_COUNT = 129 # speed bar width/speed bar block count must be int
SPEED_BAR_Y = TEXT_INPUT_Y + TEXT_INPUT_HEIGHT + 70
SPEED_BAR_WIDTH = SCREEN_WIDTH - MENU_BAR_WIDTH - 50
SPEED_BAR_BLOCK_WIDTH = int(SPEED_BAR_WIDTH/SPEED_BAR_BLOCK_COUNT)
SPEED_BAR_HEIGHT = WORD_HEIGHT/2
SPEED_BAR_TEXT_MARGIN = 5

# Options buttons
OPTION_MARGIN = 10
OPTION_BUTTON_WIDTH = MENU_BAR_WIDTH - 2*OPTION_MARGIN
OPTION_BUTTON_HELP_WIDTH = 30
OPTION_BUTTON_X_POS = SCREEN_WIDTH - MENU_BAR_WIDTH + OPTION_MARGIN
OPTION_BUTTON_WITH_HELP_WIDTH = OPTION_BUTTON_WIDTH - OPTION_MARGIN - OPTION_BUTTON_HELP_WIDTH
OPTION_BUTTON_HELP_X_POS = OPTION_BUTTON_X_POS + OPTION_BUTTON_WITH_HELP_WIDTH + OPTION_MARGIN
OPTION_HEIGHT = 30
OPTION_START_Y = 20
OPTION_DISPLAY_CAPTION_X = OPTION_BUTTON_X_POS
OPTION_DISPLAY_CAPTION_Y = 235

# Info panel
INFO_PANEL_Y = 475
INFO_PANEL_WIDTH = SCREEN_WIDTH - MENU_BAR_WIDTH
INFO_PANEL_HEIGHT = SCREEN_HEIGHT - INFO_PANEL_Y
INFO_PANEL_CAPTION_OFFSET = 10
INFO_PANEL_CAPTION_WIDTH = INFO_PANEL_WIDTH-50
INFO_PANEL_CAPTION_HEIGHT = INFO_PANEL_HEIGHT-40

# Misc
SMALL_GAP = 8
CAPTION_FONT_SIZE = 20
CAPTION_SIZE = (TEXT_INPUT_WIDTH, 50)

# Keyboard layout
TOP_ROW = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']']
MIDDLE_ROW = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'']
BOTTOM_ROW = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
KEY_WIDTH = 45
KEY_HEIGHT = KEY_WIDTH
TOP_ROW_Y = SPEED_BAR_Y + 65
KEY_X_OFFSET = 13
KEY_Y_OFFSET = 13
TOP_ROW_LENGTH = len(TOP_ROW)*KEY_WIDTH + (len(TOP_ROW)-1)*KEY_X_OFFSET
MIDDLE_ROW_X_OFFSET_FROM_TOP = 8
BOTTOM_ROW_X_OFFSET_FROM_MIDDLE = 20

# Info text
ALPHABET_INFO_TEXT = """ALPHABET MODE: This mode helps you to learn the \
position of the letters on the steno keyboard, for both right
and left keys. Type in the chord that's displayed in the "Input Chord" box. \
The highlighted keys show which keys should be
pressed. Note that if several keys are semi-lit, this means only one of them \
needs to be pressed (for example, "S-" in steno
is both "Q" and "A" in qwerty). """

WORD_INFO_TEXT = """WORD MODE: In this mode, you will start with a basic \
dictionary of words to type. As your accuracy and speed improves, 
more words will be added. Type in the chord displayed in "Input Chord" to \
enter the word."""

LESSON_INFO_TEXT = """LESSON MODE: This mode presents pre-prepared lessons. \
To select lesson, click on the ">" button to the left
of the lesson name until you see the name of the lesson you want to do. Start \
the lesson by typing the keys as prompted."""

INITIAL_TEXT = """Fly v%s: a training program for Plover, the open source \
stenography program. Hosted at https://launchpad.net/flyploverfly.
Plover by Mirabai Knight (stenographer) and Joshua Harlan Lifton \
(programmer), more info at http://stenoknight.com/plover/
NOTE: Plover should NOT be active when running this program.
Press left shift key to toggle hint options.
""" % __version__


