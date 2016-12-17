# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""The information panel which is displayed at the bottom of the screen."""

from fly import config
from fly.gui import constants as c
from fly.gui import genericelements as gel
from fly.gui import helpers as guihelpers
from fly.gui.elements import interface


class InfoPanelGUI(interface.GUIElementInterface):

    """
    Information panel showing general info, as well as specific information
    about different modes of the game.
    """

    def __init__(self):
        self.display_panel = config.DISPLAY_INFO_PANEL
        self.initial_text = c.INITIAL_TEXT
        position = (guihelpers.centred_for_x(c.INFO_PANEL_WIDTH), 
                                            c.INFO_PANEL_Y)

        self.option_panel = gel.DisplayPanel(position,
                                            (c.INFO_PANEL_WIDTH, 
                                             c.INFO_PANEL_HEIGHT), 
                                             "INFO", 
                                             c.INFO_PANEL_BACKGROUND_COLOR, 
                                             c.INFO_PANEL_TEXT_COLOR)
    
        # Text on the information panel
        position_x = guihelpers.centred_for_x(c.INFO_PANEL_WIDTH-50)
        position_y = c.INFO_PANEL_Y + c.INFO_PANEL_CAPTION_OFFSET
        self.info_caption = \
                gel.Caption((position_x, position_y), 
                            c.CAPTION_FONT_SIZE, 
                            (c.INFO_PANEL_CAPTION_WIDTH, 
                            c.INFO_PANEL_CAPTION_HEIGHT), 
                            self.initial_text,
                            text_color=c.INFO_PANEL_CAPTION_TEXT_COLOR, 
                            background_color=c.INFO_PANEL_BACKGROUND_COLOR)

    def draw(self, surface):

        """Draw info panel on screen."""

        if self.display_panel:
            self.option_panel.blit_on(surface)
            self.info_caption.blit_on(surface)

    def toggle_info_panel(self):

        """Toggle display of info panel."""

        self.display_panel = (not self.display_panel)

    def set_info(self, new_text):

        """Change the information displayed on the panel.

        @param new_text: the text to display
        @type new_text: str
        """

        self.display_panel = True
        self.info_caption.set_text(new_text)


