# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""The speed bar element which shows speed and accuracy of user input."""

from fly import config
from fly.gui import constants as c
from fly.gui import genericelements as gel
from fly.gui import helpers as guihelpers
from fly.gui.elements import interface


class SpeedBarGUI(interface.GUIElementInterface):

    """Horizontal bar on screen which fills as the speed increases.
    This speed bar is empty to start and grows as the number of words
    increases until the number of words reaches the max (set in constants).
    
    Its colour is green if accuracy is 100% and gradually goes red as accuracy
    drops.

    Additionally, the words per minute (wpm) and accuracy are displayed in a
    label on the bar.
    """
    
    def __init__(self):
        self.speed_blocks = []
        self.display_bar = config.DISPLAY_SPEED_BAR
        self.number_of_bars_to_display = 0

        self.__create_speed_bar_underlay()
        self.__create_speed_bar()

    def __create_speed_bar_underlay(self):

        """Create the base speed bar to display on screen."""

        speed_bar_x_pos = guihelpers.centred_for_x(c.SPEED_BAR_WIDTH)
        self.speed_bar_underlay = \
            gel.DisplayPanel((speed_bar_x_pos,  
                              c.SPEED_BAR_Y),
                              (c.SPEED_BAR_WIDTH, c.SPEED_BAR_HEIGHT), 
                              "SPEED/ACCURACY: ", 
                              c.SPEED_BAR_BACKGROUND_COLOR, 
                              c.SPEED_BAR_TEXT_COLOR, 
                              c.SPEED_BAR_TEXT_MARGIN)

    def __create_speed_bar(self):

        """Create the stripe that indicates speed."""

        for i in range(c.SPEED_BAR_BLOCK_COUNT):
            speed_bar_block = \
                    gel.SpeedBarBlock((guihelpers.speed_bar_pos_x(i),
                    c.SPEED_BAR_Y + 20),
                    (c.SPEED_BAR_BLOCK_WIDTH, 2),
                    (0,0,0))
            self.speed_blocks.append(speed_bar_block)

    def toggle_display(self):

        """Toggle display of speed bar."""

        self.display_bar = (not self.display_bar)

    def set_words_per_minute(self, words_per_minute):

        """Display the number of words per minute the user is typing.
        Display it in the length of the speed bar, and as a text label.

        @param words_per_minute: number of words per minute user is typing
        @type words_per_minute: float
        """

        self.speed_bar_underlay.append_text(" wpm: %s, " 
                                            % int(round(words_per_minute, 0)))
        speed_bar_len_float = min(words_per_minute/c.SPEED_BAR_MAX_SPEED, 1)
        speed_bar_length = int(c.SPEED_BAR_BLOCK_COUNT*(speed_bar_len_float))

        self.number_of_bars_to_display = int(speed_bar_length)

    def set_accuracy(self, accuracy):

        """Display the accuracy the user is typing with as fraction correct.
        Accuracy is displayed in the colour of the speed bar, and as a text
        label.

        @param accuracy: number words correct/total number of words
        @type accuracy: float
        """
    
        # Arbitrary choice of brightness
        color_brightness = 0.4

        max_eight_bit_brightness = 255
        accuracy_color = max_eight_bit_brightness*accuracy
        self.speed_bar_underlay.append_text("accuracy: %s" 
                                            % int(round((accuracy * 100), 2)))

        red = int((max_eight_bit_brightness-accuracy_color)*color_brightness)
        green = int(accuracy_color*color_brightness)
        blue = 0

        speed_bar_color = (red, green, blue)
        for speed_bar_block in self.speed_blocks:
            speed_bar_block.set_color(speed_bar_color)
    
    def draw(self, surface):

        """Draw speed bar on screen."""

        if self.display_bar:
            self.speed_bar_underlay.blit_on(surface)

            for i in range(self.number_of_bars_to_display):
                self.speed_blocks[i].blit_on(surface)


