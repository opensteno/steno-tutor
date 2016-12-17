# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Translates English words into steno chords."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import re, random, types

from fly.data import alphabetdict as alphabet
from fly.translation import ploverfacade
from fly.utils import dictionaryreader
from fly.utils import files as fileutils

import logging
logger = logging.getLogger(__name__)


CANON = "canon"
ALTERNATIVE = "alternative"
BRIEF = "brief"
MISSTROKE = "misstroke"
UNKNOWN = "unknown"


class ChordHolder(object):

    """Store all steno chords for a word, and retrieve several ways."""

    def __init__(self, chord_or_list):

        """
        @param chord: steno chord/list of steno chords
        @type chord: str (or list of str)
        """
        if type(chord_or_list) is types.ListType:
            self.chord_list = chord_or_list
        else:
            self.chord_list = [chord_or_list]

    def add_chord(self, new_chord):

        """Add new chord to list
        
        @param new_chord: steno chord
        @type new_chord: str
        """

        self.chord_list.append(new_chord)

    def get_random_chord(self):

        """All chords represent same english word. Return a chord randomly.
        
        @return: steno chord
        @rtype: str
        """

        return random.choice(self.chord_list)

    def get_canon_chord(self, categorization_dict):

        """Return canon chord if possible, or nearest alternative.
        
        @param categorization_dict: dict used to categorize chords.
            For example (dummy data only) {"PARD": "unknown", 
                                           "AUL": "canon"}
        @type categorization_dict: dict of str: str
        
        @return: steno chord
        @rtype: str
        """

        chord_categories = {}
        for chord in self.chord_list:
            if chord in categorization_dict:
                chord_category = categorization_dict[chord]
                chord_categories[chord_category] = chord
            else:
                logger.info("Uncategorized chord: %s."
                            " Please run fly.data.generation.categoriser to "
                            "categorize uncategorized words." % chord)

        if not chord_categories:
            logger.info("No categorization found for any chords, "
                        "returning random.")
            return self.get_random_chord()
        
        if CANON in chord_categories:
            return chord_categories[CANON]

        if ALTERNATIVE in chord_categories:
            return chord_categories[ALTERNATIVE]

        if UNKNOWN in chord_categories:
            logger.info("No 'canon' or 'alternative' found! Using chord with "
                        "'unknown' category %s" % chord_categories[UNKNOWN])
            return chord_categories[UNKNOWN]

        if BRIEF in chord_categories:
            logger.info("No 'canon', 'alternative' or 'unknown' found! Using "
                        "chord with 'brief' "
                        "category %s" % chord_categories[BRIEF])
            return chord_categories[BRIEF]

        if MISSTROKE in chord_categories:
            logger.info("No 'canon', 'alternative', 'unknown' or 'brief' "
                        "found! Run out of options. Using chord "
                        "with 'misstroke' "
                        "category %s" % chord_categories[MISSTROKE])
            return chord_categories[MISSTROKE]

        logger.info("Unexpected categories found: %s. Returning random "
                    "chord." % chord_categories)
        return self.get_random_chord()
                
    def get_easiest_chord(self):

        """Get the chord which is the easiest to type.
        
        @return: steno_chord
        @rtype: str
        """

        chord_points_map = {}
        for chord in self.chord_list:
            # The longer it is, the harder it is to type
            chord_points_map[chord] = 5*(1.0/len(chord))
            
            # If it has numbers, we don't want it
            if re.search('\d', chord):
                chord_points_map[chord] -= 1

            # The more strokes it has, the harder it is
            chord_points_map[chord] -= len(re.findall('/', chord))
            
        max_points = max(chord_points_map.values())
        for key, value in chord_points_map.iteritems():
            if value == max_points:
                return key

        raise RuntimeError("No chord found...this is a bug.")

    def __str__(self):

        return ", ".join(self.chord_list)


class WordToChordTranslator(object):

    """
    Translates english words to chords.
    Values (words) map to more than one key (chords). All values are 
    stored so words that all chords can be recovered.
    """

    def __init__(self, dictionary):

        """
        @param dictionary: steno to english dictionary
        @type dictionary: dict
        """

        self.inverse_dict = self.__get_inverse_dict(dictionary)
        cat_dict_path = fileutils.get_categorization_dict_path()
        self.categorization_dict = dictionaryreader.load_dict(cat_dict_path)
    
    def __get_inverse_dict(self, dictionary):

        """Return a dict of english words to chord_holders (list of chords)
        
        @param dictionary: steno to english dictionary
        @type dictionary: dict

        @return: dict of {english: chord holder with all steno representations
                 of english word}
        @rtype: {str: L{ChordHolder}}
        """

        inverse_dict = {}
        for key, value in dictionary.iteritems():
            if value in inverse_dict:
                chord_holder = inverse_dict[value]
                chord_holder.add_chord(key)
            else:
                inverse_dict[value] = ChordHolder(key)
        return inverse_dict

    def translate_from_file(self, testFile):

        """Give a file containing english words, translate to steno chords.

        @param testFile: path to file containing english words
        @type testFile: str

        @return: list of steno chords
        @rtype: list of str
        """

        with open(testFile) as f:
            data = f.readlines()
        chord_list = []

        for line in data:
            chord_line = []
            for word in self.yield_word(line):
                chord = self.translate_word(word)
                chord_line.append(chord)
            chord_list.append(' '.join(chord_line))

        return chord_list
    
    @classmethod
    def yield_word(cls, line):

        """Yield each word or punctuation mark in line.

        @param line: line of english words
        @type line: str

        @return: word or punctuation such as "?" or ":"
        @rtype: str
        """

        words = line.split(" ")
        for word in words:
            if word.find("<") != -1 or word.find(">") != -1:
                continue
            word = word.strip()
            words_or_punctuation = re.split("([-.,?;!:\"])", word)
            words_or_punctuation = [w for w in words_or_punctuation if w != '']
            for i, word_or_punctuation in enumerate(words_or_punctuation):
                if word_or_punctuation == "\"":
                    yield cls.__parse_quotes(i)
                elif cls.__is_punctuation(word_or_punctuation):
                    yield "{%s}" % word_or_punctuation
                else:
                    yield word_or_punctuation
    
    @staticmethod
    def __parse_quotes(i):
        
        """Special case for double quotation marks.
        Must figure out whether quote is opening or closing.

        @param i: index of split for double quote mark
        @type i: int

        @return: right or left double quote as appears in plover dict
        @rtype: str
        """

        if i == 0:
            return r'{"^}'
        else:
            return r'{^"}'

    @staticmethod
    def __is_punctuation(word_or_punctuation):

        """Figure out whether word_or_punctuation is word or punctuation.

        @param word_or_punctuation: english word or punctuation mark
        @type word_or_punctuation: str

        @rtype: bool
        """

        if re.search('\w+', word_or_punctuation):
            return False
        return True

    def translate_word(self, word):

        """Translate english word into steno chord equivalent.

        @param word: english word to translate
        @type word: str

        @return: random steno chord corresponding to word
        @rtype: str
        """

        first_try_handler = WordAsIs(self.inverse_dict)
        second_try_handler = WordLowerCase(self.inverse_dict)
        third_try_handler = WordPunctuationWithCaret(self.inverse_dict)
        fourth_try_handler = WordEndsApostropheEss(self.inverse_dict, 
                                                   self.categorization_dict)
        fifth_try_handler = WordIsMrOrMrs(self.inverse_dict)
        default_handler = WordUndefined(self.inverse_dict)
        
        first_try_handler.successor = second_try_handler
        second_try_handler.successor = third_try_handler
        third_try_handler.successor = fourth_try_handler
        fourth_try_handler.successor = fifth_try_handler
        fifth_try_handler.successor = default_handler

        chord_holder = first_try_handler.handle(word)
        chord = chord_holder.get_canon_chord(self.categorization_dict)
        return chord


class WordCaseHandler(object):

    """Base class for translating word or passing on to next handler."""

    def __init__(self, inverse_dict):

        """
        @param inverse_dict: dict of {english: chord holder with all steno 
                             representations of english word}
        @type inverse_dict: {str: L{ChordHolder}}
        """

        self.inverse_dict = inverse_dict

    def successor(self, successor):

        """Set WordCaseHandler to use if translation fails.

        @param successor: next word case handler
        @type successor: WordCaseHandler
        """
        
        self.successor = successor

    def handle(self, word):
        
        """Attempt to translate word and pass on if fail.

        @param word: english word to translate to steno chords
        @type word: str
        """

        pass

    def basic_handle(self, word, original_word):

        """Convenience method for trying word in dict, or passing on.

        @param word: word to find in inverse dict, may have been altered
                     from original
        @param original_word: word as was passed to first handler in chain

        @type word: str
        @type original_word: str

        @return: chord holder with all possible steno chords for word
        @rtype: L{ChordHolder}
        """

        if word in self.inverse_dict:
            return self.inverse_dict[word]
        return self.successor.handle(original_word)


class WordAsIs(WordCaseHandler):

    """Try the word just as it appears in text."""

    def handle(self, word):
        return self.basic_handle(word, word)


class WordLowerCase(WordCaseHandler):

    """Try lower case word."""

    def handle(self, word):
        return self.basic_handle(word.lower(), word)


class WordPunctuationWithCaret(WordCaseHandler):

    """Try as if the word was actually punctuation.
    If it is it appears in angle brackets in the dict."""

    def handle(self, word):
        return self.basic_handle('{%s^}' % word.strip('{}'), word)


class WordEndsApostropheEss(WordCaseHandler):

    """Try a word which ends in 's, such as "maid's". 
    "maid" is in dict, and A*ES will turn it to "maid's" 
    so append that to end.
    """
    
    def __init__(self, inverse_dict, categorization_dict):

        """
        @param inverse_dict: dict of {english: chord holder with all steno 
                             representations of english word}
        @type inverse_dict: {str: L{ChordHolder}}
        @param categorization_dict: dict used to categorize chords.
        @type categorization_dict: dict of str: str
        """

        WordCaseHandler.__init__(self, inverse_dict)
        self.categorization_dict = categorization_dict

    def handle(self, word):
        if word.endswith("'s"):
            bare_word = word.rstrip("'s")
            if bare_word in self.inverse_dict:
                chord = self.inverse_dict[bare_word].\
                        get_canon_chord(self.categorization_dict)
                if chord:
                    return ChordHolder('%s/A*ES' % chord)
        # Nope, not applicable. Move on to next handler.
        return self.successor.handle(word)


class WordIsMrOrMrs(WordCaseHandler):

    """Mr or Mrs are special cases in dict as they add a
    space and capitalize the next word. Hence they're hard
    to find. 
    """

    def handle(self, word):
        if word.find("Mr") != -1:
            if word.find("Mrs") != -1:
                return self.inverse_dict["{Mrs.}{ }{-|}"]
            return self.inverse_dict["Mr.{ }{-|}"]
        # Nope, not applicable. Move on to next handler.
        return self.successor.handle(word)


class WordUndefined(WordCaseHandler):

    """We give up. Return fingerspelled word, with original capitalization.
    
    A fingerspelled word is where letters on the left of the keyboard are
    pressed with wildcards, which acts to give the steno letter. It's like
    qwerty typing on a steno keyboard.
    """

    def handle(self, word):
        stroke_list = []
        
        for letter in word:
            # Deal with space in word (might be a brief).
            if letter == " ":
                stroke_list.append("S-P")
                continue

            if letter.isupper():
                # The user has to make it a capital letter
                stroke_list.append("KPA*")
            
            # TODO: support non-alphabet letters such as punctuation (e.g. ')
            if letter.upper() not in alphabet.STENO_ALPHABET:
                continue

            steno_letters = alphabet.STENO_ALPHABET[letter.upper()]
        
            if steno_letters.find("U") != -1 or steno_letters.find("E") != -1:
                # These two letters are to the right of the wildcard *
                stroke = '*' + steno_letters
            else:
                stroke = steno_letters + '*'
            stroke_list.append(stroke)

        return ChordHolder('/'.join(stroke_list))


if __name__ == "__main__":

    """This is so that this module can be used in an alias if desired.
    For example:

    alias is='cd dir/where/I/put/fly; python -m translation.wordstochords '

    Then typing 'is love' in the terminal (where you want the steno chord for 
    'love') will provide: HOF
    """ 

    plover_control = ploverfacade.PloverControl()
    dict_filename = fileutils.get_plover_dict_path()
    dictionary = dictionaryreader.load_dict(dict_filename)

    translator = WordToChordTranslator(dictionary)
    word = sys.argv[1]
    print(translator.translate_word(word))


