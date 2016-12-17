# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Generic elements such as buttons and captions."""

import pygame
import logging
logger = logging.getLogger(__name__)

from fly import config
from fly.gui import constants


class DrawableElementInterface(pygame.Surface):

    """Interface that all drawable elements must conform to."""

    def blit_on(self, surface):

        """Draw element on screen.

        @param surface: the screen to draw on
        @type surface: pygame.Surface
        """

        raise NotImplementedError("Child classes should implement "
                                  "this method!")


class Caption(DrawableElementInterface):

    """Box with text. The text will change during the life of the element."""
    
    def __init__(self, pos, font_size, size, text, margin=0, 
                 text_color=constants.CAPTION_TEXT_COLOR, 
                 background_color=constants.CAPTION_BACKGROUND_COLOR):
        
        """
        @param pos: position on screen (x, y)
        @param font_size: size of font on label
        @param size: size of box around label
        @param text: words on label
        @param margin: offset text into box
        @param text_color: colour of label text
        @param background_color: colour of box label is in

        @type pos: tuple of (int, int)
        @type font_size: int
        @type size: tuple of (int, int)
        @type text: str
        @type margin: int
        @type text_color: tuple (int, int, int) representing red,
                          green, blue where each is between 0 and 255
        @type background_color: tuple (int, int, int) representing red,
                          green, blue where each is between 0 and 255
        """

        DrawableElementInterface.__init__(self, size)
        
        self.text = text
        self.pos = pos
        self.size = size
        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color
        self.display_text = True
        
        self.margin = margin
    
    def blit_on(self, surface):

        """Draw element on screen."""
        
        self.fill(self.background_color)
        font = pygame.font.Font(None, self.font_size)
        
        if self.display_text:
            line_number = 0

            # Handle multi-line text
            text_lines = self.text.split("\n")
            for line in text_lines:
                text = font.render(line, 1, self.text_color)
                self.blit(text, (self.margin, self.margin)) 
                line_number += 1
                blit_here = (self.pos[0], self.pos[1] + \
                             line_number*self.font_size)
                surface.blit(self, blit_here)
                self.fill(self.background_color)

    def set_text(self, word):

        """Set text in caption to word.

        @param word: which text to set caption to
        @type word: str
        """

        if word is None:
            word = ""
        self.text = word


class KeyboardKey(DrawableElementInterface):
    
    def __init__(self, pos, size, caption="", steno_caption="", 
                 color=constants.QWERTY_KEY_BACKGROUND_COLOR, 
                 text_color=constants.QWERTY_KEY_TEXT_COLOR, 
                 steno_color=constants.STENO_KEY_TEXT_COLOR):

        """
        @param pos: position on screen (x, y)
        @param size: size of box around label
        @param caption: qwerty key label
        @param steno_caption: steno key label
        @param color: colour of key
        @param text_color: colour of qwerty label text
        @param steno_color: colour of steno label text

        @type pos: tuple of (int, int)
        @type size: tuple of (int, int)
        @type caption: str
        @type steno_caption: str
        @type color: tuple (int, int, int) representing red,
                     green, blue where each is between 0 and 255
        @type text_color: tuple (int, int, int) representing red,
                          green, blue where each is between 0 and 255
        @type steno_color: tuple (int, int, int) representing red,
                           green, blue where each is between 0 and 255
        """

        DrawableElementInterface.__init__(self, size)
    
        self.onclick = None
        self.toggle_hint = False
    
        self.pressed = False
        self.lit = False
        self.partial_lit = False
        self.steno_tint_color = None 
        self.original_color = color
        
        self.caption = caption
        self.steno_caption = steno_caption
        self.pos = pos
        self.size = size
        self.color = color
        self.text_color = text_color
        self.steno_color = steno_color
        self.margin = constants.KEY_WIDTH/8.0
        self.font_size = constants.KEY_WIDTH/2.0

        self.display_qwerty = config.DISPLAY_QWERTY_KEYS
        self.display_steno = config.DISPLAY_STENO_KEYS
        self.highlight_keys = config.DISPLAY_KEY_HIGHLIGHTING
        
        self.recolor_keys()

    def recolor_keys(self):

        """Calculate the color of the key based on the steno tint color."""

        if self.steno_tint_color and self.highlight_keys:
            self.color = constants.STINT_QWERTY_KEY_BACKGROUND_COLOR
            self.text_color = constants.STINT_QWERTY_KEY_TEXT_COLOR
            self.steno_color = constants.STINT_STENO_KEY_TEXT_COLOR

            self.lit_color = self.steno_tint_color
            self.partial_lit_color = self.lit_color
        
            pressed_red = min(self.steno_tint_color[0] + 50, 255)
            pressed_green = min(self.steno_tint_color[1] + 50, 255)
            pressed_blue = min(self.steno_tint_color[2] + 50, 255)
            self.pressed_color = (pressed_red, pressed_green, pressed_blue)

        else:
            self.color = constants.QWERTY_KEY_BACKGROUND_COLOR
            self.text_color = constants.QWERTY_KEY_TEXT_COLOR
            self.steno_color = constants.STENO_KEY_TEXT_COLOR

            pressed_red = max(self.color[0] - 50, 0)
            pressed_green = max(self.color[1] - 50, 0)
            pressed_blue = max(self.color[2] - 50, 0)
            self.pressed_color = (pressed_red, pressed_green, pressed_blue)
        
            lit_red = min(self.color[0] + constants.KEY_LIT_INCREMENT[0], 255)
            lit_green = min(self.color[1] + constants.KEY_LIT_INCREMENT[1], 255)
            lit_blue = min(self.color[2] + constants.KEY_LIT_INCREMENT[2], 255)
            self.lit_color = (lit_red, lit_green, lit_blue)

            partial_red = min(self.color[0] + constants.PARTIAL_LIT_INCREMENT[0], 255)
            partial_green = min(self.color[1] + constants.PARTIAL_LIT_INCREMENT[1], 255)
            partial_blue = min(self.color[2] + constants.PARTIAL_LIT_INCREMENT[2], 255)
            self.partial_lit_color = (partial_red, partial_green, partial_blue)

    def blit_on(self, surface):

        """Draw element on screen."""

        self.recolor_keys()
        self.fill(self.color)
        if self.highlight_keys:
            if self.lit: 
                self.fill(self.lit_color)
            if self.partial_lit:
                self.fill(self.partial_lit_color)
            if self.pressed:
                self.fill(self.pressed_color)
            
        font = pygame.font.Font(None, int(self.font_size))
        if self.caption and self.display_qwerty:
            text = font.render(self.caption, 1, self.text_color)
            self.blit(text, (self.margin,self.margin))
       
        if self.steno_caption and self.display_steno:
            # This sets the steno text to black for highlighted keys--easier
            # to read!
            if self.highlight_keys and self.steno_tint_color and \
               (self.lit or self.partial_lit):
                self.steno_color = (0, 0, 0)
            elif self.highlight_keys and (self.lit or self.partial_lit):
                self.steno_color = constants.HIGHLIGHTED_KEY_TEXT_COLOR

            # Render the steno label on the screen
            steno_text = font.render(self.steno_caption, 1, self.steno_color)
            self.blit(steno_text, 
                      (constants.KEY_WIDTH-self.font_size/2.0-self.margin, 
                       constants.KEY_WIDTH-self.font_size/2.0-self.margin))
        surface.blit(self, self.pos)

    def toggle_qwerty_display(self):

        """Toggle the display of the qwerty label on key."""

        self.display_qwerty = (not self.display_qwerty)

    def toggle_steno_display(self):

        """Toggle the display of the steno label on key."""

        self.display_steno = (not self.display_steno)

    def toggle_highlight(self):

        """Toggle whether the key is capable of displaying highlighted."""

        self.highlight_keys = (not self.highlight_keys)
        
    def contains(self, pos):

        """Used for determining whether mouse is over key.
        
        @param pos: position on screen (x, y)
        @param pos: tuple of (int, int)

        @return: whether position given is over element.
        @rtype: bool
        """

        return (pos[0] >= self.pos[0] and \
                pos[1] >= self.pos[1] and \
                pos[0] <= self.pos[0]+self.size[0] and \
                pos[1] <= self.pos[1]+self.size[1])
    
    def set_pressed(self, key):

        """Set the key as being pressed by user.

        @param key: code of key user has pressed.
        @type key: int
        """

        if key == 91:
            if self.caption == "[":
                self.pressed = True
        elif key == 93:
            if self.caption == "]":
                self.pressed = True
        elif key == 304: # Left shift
            self.toggle_hint = True
        elif key in range(256):
            if self.caption.lower() == chr(key):
                self.pressed = True
        else:
            logger.warning("Unknown key %s" % key)


class DisplayPanel(DrawableElementInterface):

    """A panel with text that does not interact with user."""
    
    def __init__(self, pos, size, caption="", color=(100,100,100), 
                 text_color=(0,0,0), margin=10):

        """
        @param pos: position on screen (x, y)
        @param size: size of box around label
        @param caption: words on panel
        @param color: background colour of panel
        @param text_color: colour of text on panel
        @param margin: offset from panel borders for text

        @type pos: tuple of (int, int)
        @type size: tuple of (int, int)
        @type caption: str
        @type color: tuple (int, int, int) representing red,
                     green, blue where each is between 0 and 255
        @type text_color: tuple (int, int, int) representing red,
                          green, blue where each is between 0 and 255
        @type margin: int
        """

        DrawableElementInterface.__init__(self, size)
    
        self.caption = caption
        self.text = self.caption

        self.pos = pos
        self.size = size
        self.color = color
        self.text_color = text_color
        
        self.margin = margin

    def append_text(self, text):

        """Add text to existing text on panel label.
        
        @param text: text to add
        @type text: str
        """

        self.text += text

    def blit_on(self, surface):

        """Draw panel on screen."""

        self.fill(self.color)
            
        font = pygame.font.Font(None, 16)
        text = font.render(self.text, 1, self.text_color)
        self.blit(text, (self.margin,self.margin))
        surface.blit(self, self.pos)
        self.text = self.caption


class SpeedBarBlock(DrawableElementInterface):

    """A segment of the stripe in the speed bar.

    Although the speed bar looks like a single element, it is made up of
    multiple blocks. This represents a single block. Setting the color will
    set the colour of the speed bar stripe.
    """
    
    def __init__(self, pos, size, color):

        """
        @param pos: position on screen (x, y)
        @param size: size of speed bar block
        @param color: colour of speed bar block

        @type pos: tuple of (int, int)
        @type size: tuple of (int, int)
        @type color: tuple (int, int, int) representing red,
                     green, blue where each is between 0 and 255
        """

        DrawableElementInterface.__init__(self, size)
    
        self.pos = pos
        self.color = color

    def set_color(self, new_color):

        """Change color of speed bar block to new_color.

        @param new_color: color to make speed bar block
        @type new_color: tuple (int, int, int) representing red,
                         green, blue where each is between 0 and 255
        """

        self.color = new_color
        
    def blit_on(self, surface):

        """Draw speed bar block on screen."""

        self.fill(self.color)
        surface.blit(self, self.pos)


class Button(DrawableElementInterface):

    """Box with text that the user can click on, such as an option button."""
    
    def __init__(self, pos, size, caption="", 
                 color=(100,100,100), text_color=(0,0,0)):

        """
        @param pos: position on screen (x, y)
        @param size: size of box around label
        @param caption: words on label
        @param color: colour of button
        @param text_color: colour of label text

        @type pos: tuple of (int, int)
        @type size: tuple of (int, int)
        @type caption: str
        @type color: tuple (int, int, int) representing red,
                     green, blue where each is between 0 and 255
        @type text_color: tuple (int, int, int) representing red,
                          green, blue where each is between 0 and 255
        """

        DrawableElementInterface.__init__(self, size)
    
        self.onclick = None
        self.active = False
        self.display = True
    
        self.pressed = False
        self.hover = False
        
        self.caption = caption
        self.pos = pos
        self.size = size
        self.color = color
        self.text_color = text_color
        
        self.margin = 10

        pressed_red = min(self.color[0]+constants.BUTTON_PRESSED_INCREMENT[0], 255)
        pressed_green = min(self.color[1]+constants.BUTTON_PRESSED_INCREMENT[1], 255)
        pressed_blue = min(self.color[2]+constants.BUTTON_PRESSED_INCREMENT[2], 255)
        self.pressed_color = (pressed_red, pressed_green, pressed_blue)

        hover_red = min(self.color[0]+constants.BUTTON_HOVER_INCREMENT[0], 255)
        hover_green = min(self.color[1]+constants.BUTTON_HOVER_INCREMENT[1], 255)
        hover_blue = min(self.color[2]+constants.BUTTON_HOVER_INCREMENT[2], 255)
        self.hover_color = (hover_red, hover_green, hover_blue)
        self.active_color = self.hover_color 

    def set_active(self, value):

        """Whether to set button as active.

        @param value: what to set button to.
        @type value: bool
        """

        self.active = value
    
    def blit_on(self, surface):

        """Draw button on screen."""

        if self.display:
            self.fill(self.color)
            if self.hover: 
                self.fill(self.hover_color)
            if self.pressed:
                self.fill(self.pressed_color)
            if self.active:
                self.fill(self.active_color)
                
            font = pygame.font.Font(None, 16)
            text = font.render(self.caption, 1, self.text_color)
            self.blit(text, (self.margin,self.margin))
            surface.blit(self, self.pos)

    def set_text(self, new_caption):

        """Set button text to new_caption.

        @param caption: new text to set button label to
        @type caption: str
        """

        self.caption = new_caption
        
    def contains(self, pos):
        
        """Used for determining whether mouse is over key.
        
        @param pos: position on screen (x, y)
        @param pos: tuple of (int, int)

        @return: whether position given is over element.
        @rtype: bool
        """

        contains = (pos[0] >= self.pos[0] and \
                    pos[1] >= self.pos[1] and \
                    pos[0] <= self.pos[0]+self.size[0] and \
                    pos[1] <= self.pos[1]+self.size[1])
        return contains


