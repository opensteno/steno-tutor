# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""
Maps lessons to word chooser, where each lesson knows how it will be presented.

Lessons have retrieval and display directives that determine how they will be
presented. Word choosers are what determines the behaviour of the model, so 
lessons will be assigned a word chooser that fits their directives.
"""

import logging
logger = logging.getLogger(__name__)

from fly.models.wordchooser import randomize
from fly.models.wordchooser import incremental
from fly.models.wordchooser import inorder
from fly.lessons.helpers.directive import DirectiveInterpreter


class LessonWordChooserMapper(object):

    """Maps lesson to word chooser based on information in lesson object."""

    # Map retrieval directives to word choosers.
    RETRIEVAL_MAP = {DirectiveInterpreter.RETRIEVAL_RANDOMIZE_DIRECTIVE:\
                                    randomize.RetrieveRandomize,
                     DirectiveInterpreter.RETRIEVAL_INCREMENT_DIRECTIVE:\
                                    incremental.RetrieveIntroduceIncrement,
                     DirectiveInterpreter.RETRIEVAL_IN_ORDER_DIRECTIVE:\
                                    inorder.RetrieveInOrder}

    def get_word_chooser(self, lesson):

        """Retrieve a word chooser that is appropriate to the lesson.
        
        @param lesson: lesson object to populate.
        @type lesson: L{lessons.container.Lesson}

        @return: word chooser
        @rtype: class implementing L{models.wordchooser.interface}
        """

        retrieval_directive = lesson.retrieval_directive
        display_directive = lesson.display_directive

        # This isn't an ideal way of implementing the sentence display 
        # directive, but since for now it's supported for in_order retrieval,
        # it'll do.
        sentence_directive = DirectiveInterpreter.DISPLAY_SENTENCE_DIRECTIVE
        in_order_directive = DirectiveInterpreter.RETRIEVAL_IN_ORDER_DIRECTIVE
        if display_directive == sentence_directive:
            if retrieval_directive != in_order_directive: 
                logger.warning("Currently sentence directive can only be "
                               "used with in_order display directive. "
                               "Ignoring sentence directive.")
            else:
                return inorder.RetrieveInOrderSentence(lesson)

        return self.RETRIEVAL_MAP[retrieval_directive]\
                                (lesson.chord_translation_dict, 
                                 lesson.chords_list)
        

