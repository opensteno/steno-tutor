# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""The text that appears on the screen while the GUI elements are loading."""

from fly.gui import genericelements
from fly.gui import constants


class StartupCaption(object):

    """Progress caption to tell the user how much of the game has loaded."""

    def __init__(self):
        font_size = 45
        size = (230, 200)
        pos = (constants.SCREEN_WIDTH/2. - size[0]/2., 
               constants.SCREEN_HEIGHT/2. - size[1]/2.)
        text = "Loading"
        self.caption = genericelements.Caption(pos, font_size, size, text)

    def display(self, screen, text):

        """Set the new text, and display on screen.

        @param screen: surface to blit on
        @param text: text to display
        
        @type screen: pygame.Surface
        @type text: str
        """

        self.caption.set_text(text)
        self.caption.blit_on(screen)


