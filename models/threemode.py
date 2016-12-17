# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""
Fly runs with three models: Alphabet, Word, and Lesson. This
module configures the game model to create these models.
"""

from fly.models import gamemodel as game_model
from fly.models.wordchooser import leveldicts, randomize
from fly.models.inputinterpreter import alphabet as input_alphabet
from fly.models.inputinterpreter import word as input_word
from fly.data import alphabetdict as ad


ALPHABET_MODEL_NAME = "alphabet"
WORD_MODEL_NAME = "word"
LESSON_MODEL_NAME = "lesson"


def get_alphabet_model():

    """Create game model to use for alphabet model.

    @return: model configured for alphabet
    @rtype: L{game_model.GameModel)
    """

    alpha_word_list = [] # Dummy, not used
    steno_dict = ad.INVERSE_STENO.pop("*")
    alpha_word_chooser = randomize.RetrieveRandomize(ad.INVERSE_STENO, 
                                                     alpha_word_list)
    alpha_interpreter = input_alphabet.InterpretForAlphabet()
    alphabet_model = game_model.GameModel(ALPHABET_MODEL_NAME, 
                                          alpha_word_chooser, 
                                          alpha_interpreter)

    return alphabet_model


def get_word_model():

    """Create game model to use for word model.

    @return: model configured for word
    @rtype: L{game_model.GameModel)
    """

    level_dict_word_chooser = leveldicts.RetrieveFromLevelDictionaries()
    word_interpreter = input_word.InterpretForWord()
    word_model = game_model.GameModel(WORD_MODEL_NAME, 
                                      level_dict_word_chooser,
                                      word_interpreter)
    return word_model


def get_lesson_model(gui, lesson_control):

    """Create game model to use for lesson model.

    @return: model configured for lesson
    @rtype: L{game_model.GameModel)
    """

    lesson = gui.get_current_lesson_name()
    word_chooser = lesson_control.get_word_chooser(lesson)
    if word_chooser:
        lesson_word_chooser = word_chooser
    else:
        lesson_word_chooser = leveldicts.RetrieveFromLevelDictionaries()

    word_interpreter = input_word.InterpretForWord()

    lesson_model = game_model.GameModel(LESSON_MODEL_NAME,
                                        lesson_word_chooser,
                                        word_interpreter)
    return lesson_model
       

