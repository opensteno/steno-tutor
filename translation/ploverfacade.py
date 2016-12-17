# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""For Fly to call plover, it must go through this file."""

import logging
logger = logging.getLogger(__name__)

from fly.plover import steno
from fly.plover import machine
from fly.plover import config as conf
from fly.plover.dictionary import eclipse as dictionary_module
from fly.plover.machine import base

# Won't register as instance of sidewinder.Stenotype if from fly
from plover.machine import sidewinder

from fly.utils import dictionaryreader, files as fileutils


class PloverControl(object):

    """Wrap the creation of steno machine, and a translator."""
    
    def __init__(self):
        self.dictionary = None
        self.running = False
        self.machine_init = {}

    def set_up_steno(self, translation_callback_function):

        """Start a steno machine that will intercept keystrokes and translate.

        @param translation_callback_function: function that uses translation.
            Should take a translation object L{plover.steno.Translation} and
            an overflow.
        @type translation_callback_function: function
        """
       
        machine_module = self.get_machine_module()
        self.steno_machine = machine_module.Stenotype(**self.machine_init)
        self.translation_callback_function = translation_callback_function

        dict_filename = fileutils.get_plover_dict_path()
        self.dictionary = dictionaryreader.load_dict(dict_filename)
        self.translator = self.create_translator(self.dictionary)

    def get_machine_module(self):

        """Set the machine module and any initialization variables.

        @return: the machine module for the steno machine that the user is
                 running (set in the config of plover).
        @rtype: machine module such as machine.sidewinder
        """

        config = conf.get_config()
        machine_type = config.get(conf.MACHINE_CONFIG_SECTION,
                                       conf.MACHINE_TYPE_OPTION)
        machine_module = conf.import_named_module(machine_type,
                                                       machine.supported)
        if machine_module is None:
            raise ValueError('Invalid configuration value for %s: %s' %
                             (conf.MACHINE_TYPE_OPTION, machine_type))
        if issubclass(machine_module.Stenotype,
                      base.SerialStenotypeBase):
            serial_params = conf.get_serial_params(machine_type, config)
            self.machine_init.update(serial_params.__dict__)

        return machine_module

    def get_dictionary(self):

        """Get plover's dictionary.

        @return: steno to english dictionary
        @rtype: dict
        """

        if not self.dictionary:
            logger.error("Dictionary missing...check set_up_steno has been "
                         "called.")
        return self.dictionary

    def create_translator(self, dictionary):

        """Create a steno translator and return it. Add callback function.

        @param dictionary: steno to english dictionary
        @type dictionary: dict

        @return: plover translator object
        @rtype: L{plover.steno.Translator}
        """

        translator = steno.Translator(self.steno_machine, dictionary, 
                                      dictionary_module)
        translator.add_callback(self.translation_callback_function)
        return translator

    def start(self):

        """Start translating!"""

        self.steno_machine.start_capture()

    def stop(self):

        """Stop translating."""

        self.steno_machine.stop_capture()

    def suspend(self):

        """Temporarily stop translating."""

        if isinstance(self.steno_machine, sidewinder.Stenotype):
            self.steno_machine.is_keyboard_suppressed = False
    
    def resume(self):

        """Resume running after machine has been suspended."""
   
        if isinstance(self.steno_machine, sidewinder.Stenotype):
            self.steno_machine.is_keyboard_suppressed = True


def get_ordering(steno_key):

    """Find out the key order of the steno_key provided.
    This is a numerical ordering of where it sits on the keyboard
    in relation to other keys.

    @param steno_key: steno key char such as 'T-' or '-S'
    @type steno_key: str

    @return: ordering on keyboard
    @rtype: int
    """

    if steno_key[-1] != '-' and steno_key[0] != '-':
        steno_key_left = steno_key + '-'

        # More likely it's a left hand key, if it was right, 
        # it's usually indicated.
        if steno_key_left in steno.STENO_KEY_ORDER:
            steno_key = steno_key_left
        
        if steno_key.find("A") != -1:
            steno_key = "A-"
        if steno_key.find("E") != -1:
            steno_key = "-E"
        if steno_key.find("U") != -1:
            steno_key = "-U"
        if steno_key.find("O") != -1:
            steno_key = "O-"
    
    return steno.STENO_KEY_ORDER[steno_key]


