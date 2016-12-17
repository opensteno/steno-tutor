#!/usr/bin/python
# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Main module for running Fly."""

import os
import sys

# Hack so that all modules can be imported from Fly, 
# but the game can still be run just by calling
# this as a script.
sys.path.append(os.path.dirname(os.getcwd()))

import pygame
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fly import __version__
from fly.translation import ploverfacade
from fly.models import threemode
from fly.lessons import control
from fly.statistics import gatherer
from fly.gui import startup as startup_caption
from fly.gui import constants
from fly.gui import collection


# Global variables, so can be accessed in main
translation = ""
chord = ""


def translation_received(translationObj, overflow):

    """
    Callback function used to listen to plover's interpretation of key presses.

    This is used to set global variables that can be read by the models when 
    needed.

    @param translationObj: A data model for the mapping between a sequence of
                           strokes and a string. 
    @param overflow: unused.

    @type translationObj: L{plover.steno.Translation}
    @type overflow: unused.
    """

    global translation, chord
    translation = translationObj.english
    chord = translationObj.rtfcre


class Main(object):

    """This class runs Fly."""
    
    def __init__(self):

        logging.info("Started!")

        # Centre window on screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Set up screen
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, 
                                               constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Fly, Plover, Fly! "
                                   "v%s" % __version__)
        self.screen.fill(constants.CANVAS_COLOR)

        # Display "Loading [X%]" caption on screen before GUI displays, as game
        # can take a while to load.
        self.startupCaption = startup_caption.StartupCaption()
        self.update_startup_caption("Loading [0%]")

        # Set up plover
        self.plover_control = ploverfacade.PloverControl()
        self.plover_control.set_up_steno(translation_received)
        dictionary = self.plover_control.get_dictionary()

        # Set up lesson reading and statistics
        self.lesson_control = control.LessonControl(dictionary)
        self.stats = gatherer.StatisticGatherer()

        # Set up GUI
        lesson_names = self.lesson_control.get_lesson_names()
        self.gui = collection.ElementsCollection(lesson_names)
       
        # Load models
        self.alphabet_model = threemode.get_alphabet_model()
        self.update_startup_caption("Loading [33%]")
        self.word_model = threemode.get_word_model() 
        self.update_startup_caption("Loading [66%]")
        self.lesson_model = threemode.get_lesson_model(self.gui,
                                                       self.lesson_control)
        self.update_startup_caption("Loading [100%]")

        self.model = self.alphabet_model
        self.current_model_name = self.model.name

    def update_startup_caption(self, text):

        """Set caption on screen to display specified text.
        
        @param text: text to display
        @type text: str
        """

        self.startupCaption.display(self.screen, text)
        pygame.display.update()

    def run(self):

        """Run the main loop of the game after starting plover.

        In a try/finally so that plover will always be stopped whether
        there's an error or the user exits normally.
        """

        try:
            self.plover_control.start()
            self.new_word_to_type()

            running = True
            while running:
                running = self.main_loop()

        finally:
            self.plover_control.stop()

    def main_loop(self):

        """This is executed as long as the game runs."""

        global translation, chord
        self.gui.reset()

        # Tell model about user input.
        self.model.set_input_word_and_translation(chord, translation)

        # Give model a chance to alter word and translation in case what plover
        # provided is not what the model wants.
        word_and_trans = self.model.get_chord_and_translation()

        # Display user input.
        self.gui.set_input_word_and_translation(word_and_trans[0], 
                                                word_and_trans[1])
        self.set_translation_blank()
    
        # Check for mouse clicks or key presses etc.
        running = self.process_events()
        if not running:
            return False

        self.gui.act_on_hint_key_press()
       
        # Display word user should type.
        self.gui.show_word_to_type(self.model.get_qwerty_letters_to_type())
        if self.model.right_word_entered():
            self.model.clear_inputs()
            self.gui.on_right_word_entered()
            self.stats.on_right_word_entered()

            # Reset with new word
            self.new_word_to_type()

        elif self.model.wrong_word_entered():
            # Record that a wrong word was entered for the accuracy count.
            self.stats.on_wrong_word_entered()

        else:
            # Word has not been completed
            pass
        
        # Update speed bar
        words_per_minute = self.stats.get_words_per_min()
        accuracy = self.stats.get_fraction_accurate()
        self.gui.update_speed_bar(words_per_minute, accuracy)
       
        # Update display
        self.screen.fill(constants.CANVAS_COLOR)
        self.gui.draw(self.screen)
        pygame.display.flip()

        # Switch model if user has changed models
        self.switch_model()

        # Set level (up or down)
        level = self.stats.get_level()
        self.model.switch_level(level)

        # Set the lesson model word chooser based on the lesson chosen in UI.
        # Only applies to the game if lesson model in use.
        lesson = self.gui.get_current_lesson_name()
        word_chooser = self.lesson_control.get_word_chooser(lesson)
        if word_chooser:
            self.lesson_model.set_word_chooser(word_chooser)
            self.new_word_to_type()

        return True

    def new_word_to_type(self):

        """Generate a new word for the user to type."""

        self.model.generate_word_to_type()
        target_chord, target_translation = \
                self.model.get_display_word_and_translation() 
        self.gui.set_word_to_type(target_chord, target_translation)
    
    def switch_model(self):

        """Check which model the GUI is set to and switch if necessary."""

        model_name = self.gui.get_model_to_use()
        if model_name == self.model.name:
            return

        if model_name == threemode.ALPHABET_MODEL_NAME:
            self.model = self.alphabet_model
        elif model_name == threemode.WORD_MODEL_NAME:
            self.model = self.word_model
        else:
            self.model = self.lesson_model
        
        self.new_word_to_type()

    def process_events(self):

        """Check if any events have been triggered and process them."""

        for event in pygame.event.get():
            if self.event_is_quit(event):
                return False
            
            elif self.event_is_lose_focus(event):
                self.plover_control.suspend()
                pass

            elif self.event_is_gain_focus(event):
                self.plover_control.resume()
                pass
                
            elif self.event_is_mouse_motion(event):
                self.gui.on_mouse_motion(event)

            elif self.event_is_left_mouse_button_down(event):
                self.gui.on_right_mouse_down(event)

            elif self.event_is_left_mouse_button_up(event):
                self.gui.on_right_mouse_up(event)

            elif self.event_is_key_down(event):
                self.gui.on_key_down(event)

        return True

    def event_is_quit(self, event):
        """Return True if event is quit game"""
        return event.type == pygame.QUIT

    def event_is_lose_focus(self, event):
        """Return True if window has just lost focus."""
        return event.type == pygame.ACTIVEEVENT and event.gain == 0
                
    def event_is_gain_focus(self, event):
        """Return True if window has just gained focus."""
        return event.type == pygame.ACTIVEEVENT and event.gain == 1

    def event_is_mouse_motion(self, event):
        """Return True if event is mouse motion."""
        return event.type == pygame.MOUSEMOTION
    
    def event_is_left_mouse_button_down(self, event):
        """Return True if the left mouse button is down"""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

    def event_is_left_mouse_button_up(self, event):
        """Return True if the left mouse button has been released."""
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1

    def event_is_key_down(self, event):
        """Return True if a key is pressed."""
        return event.type == pygame.KEYDOWN

    def set_translation_blank(self):
        """Clear global chord and translation ready for new user input."""
        global translation, chord
        translation = ""
        chord = ""


if __name__ == "__main__":

    main = Main()
    main.run()


