# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Interface for all GUI elements."""


class GUIElementInterface(object):

    """Interface for GUI elements. Not all methods need be implemented."""
    
    def draw(self, surface):

        """Paint element on surface.

        @param surface: screen to draw on
        @type surface: pygame.Surface
        """

        pass
    
    def reset(self):

        """Return element to initial state."""

        pass
    
    def on_mouse_motion(self, event):

        """Respond to mouse motion event.

        @param event: mouse motion event
        @type event: pygame.event
        """

        pass

    def on_right_mouse_down(self, event):
        
        """Respond to right mouse button click down event.

        @param event: mouse button down event
        @type event: pygame.event
        """

        pass

    def on_right_mouse_up(self, event):
        
        """Respond to right mouse button release event.

        @param event: mouse button up event
        @type event: pygame.event
        """

        pass

    def on_key_down(self, event):

        """Respond to key press event.

        @param event: key press down event
        @type event: pygame.event
        """

        pass
        

