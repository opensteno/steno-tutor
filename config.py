# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Configurable game options."""

"""Color options"""
# Available colour schemes: "classic", "light", "highcontrast"
COLOR_SCHEME = "classic"

"""Initial display settings"""
# Display word and translation side by side
# This can be toggled in the GUI with "Toggle Word/Sentence"
WORD_STYLE = False

# Display speed bar
# This can be toggled in the GUI with "Toggle Speed Display"
DISPLAY_SPEED_BAR = True

# Display info
# This can be toggled in the GUI with "Toggle Info Display"
DISPLAY_INFO_PANEL = True

# Display key highlighting
# This can be toggled in the GUI with "Toggle Key Highlighting"
DISPLAY_KEY_HIGHLIGHTING = True

# Display input chord
# This can be toggled in the GUI with "Toggle Input Chord Display"
DISPLAY_INPUT_CHORD = True

# Display steno keys on onscreen keyboard
# This can be toggled in the GUI with "Toggle Steno Display"
DISPLAY_STENO_KEYS = True

# Display qwerty keys on onscreen keyboard
# This can be toggled in the GUI with "Toggle QWERTY Display"
DISPLAY_QWERTY_KEYS = False

# Tint steno key combinations colors to reinforce mapping between
# keys and english alphabet
# This can be toggled in the GUI with "Toggle Steno Color"
DISPLAY_STENO_COLOR = False

# Pressing left shift key will toggle these options in the display
# Use comma separated values for any of the following:
# "KeyHighlighting, KeyStenoText, ChordToTypeDisplay"
# For example for keyhighlighting only toggled "KeyHighlighting"
# Or for chord to type and steno text label display toggled:
# "KeyStenoText, ChordToTypeDisplay"
HINT_OPTIONS="KeyHighlighting, ChordToTypeDisplay"

"""Levelling up and down"""
# How many words should be presented before the user can change levels?
WORDS_DELTA_TO_LEVEL_UP = 5

# What is the minimum accuracy the user must attain to level up?
ACCURACY_FRACTION_THRESHOLD = 0.5

# How many words per minute must a user type to level up? 
SPEED_WORDS_PER_MIN_THRESHOLD = 20

"""For lessons with <introduce_increment> retrieval directive only"""
# How many words should be in list at start
BASE_WORD_NUMBER = 5

# Number of words that must be correct before new word added
WORDS_BEFORE_WORD_ADDED = 5

"""For lessons only"""
# Force translation of lesson files to chords when Fly starts, even if 
# translation files already exist (useful only if code has changed)
FORCE_LESSON_REGENERATION = False


