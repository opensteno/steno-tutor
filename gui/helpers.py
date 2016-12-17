# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Helper functions for placement of GUI elements"""

from fly.gui import constants


def centred_for_x(element_length):

    """Return pos x centred in the main area (excluding right menu bar)
    
    @param element_length: width of element to centre
    @type element_length: int

    @return: x coordinate which will centre element on screen (excluding
            right menu bar)
    @rtype: float
    """

    width_main_area = constants.SCREEN_WIDTH - constants.MENU_BAR_WIDTH
    return 0.5*(width_main_area - element_length)


def centred_for_half_x(element_length, left_screen_half=True):

    """Return pos x half centred in the main area (excluding right menu bar)
    This centres the given element in the left or right half of the remaining
    area once the right menu bar has been removed.

    @param element_length: width of element to centre
    @param left_screen_half: whether the element is on the left or right half

    @type element_length: int
    @type left_screen_half: bool

    @return: x coordinate which will centre element on left or right of the 
             screen (excluding right menu bar)
    @rtype: float
    """

    half_x = (1.0/3.0)*((constants.SCREEN_WIDTH-constants.MENU_BAR_WIDTH) \
             - 2*element_length)
    if left_screen_half:
        return half_x
    else:
        return 2*half_x + element_length


def speed_bar_pos_x(speed_block_number):

    """For a speed block from the line up that forms the bar, return x pos.
    
    @param speed_block_number: where 0 is leftmost bar, 1 is next to it on 
                               the right, and so on.
    @type speed_block_number: int

    @return: x coordinate for the speed block
    @rtype: float
    """

    return centred_for_x(constants.SPEED_BAR_WIDTH) + \
            speed_block_number*constants.SPEED_BAR_BLOCK_WIDTH


