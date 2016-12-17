# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""
Manage directives, which are the first line of the lesson files.
These dictate how the lesson should be presented.
"""

import re


class DirectiveInterpreter(object):

    """
    Lesson files have directives at the top describing what methods of 
    retrieval and display they want to support. This class reads and 
    analyzes them.
    """
    
    # Names of directives expected to appear in lesson file
    # first line e.g. <randomize>
    RETRIEVAL_RANDOMIZE_DIRECTIVE = 'randomize'
    RETRIEVAL_INCREMENT_DIRECTIVE = 'introduce_increment'
    RETRIEVAL_IN_ORDER_DIRECTIVE = 'in_order'

    DISPLAY_WORD_DIRECTIVE = 'word'
    DISPLAY_SENTENCE_DIRECTIVE = 'sentence'
    
    # List of all supported retrieval directives, i.e. how word is retrieved.
    RETRIEVAL_DIRECTIVES = [RETRIEVAL_RANDOMIZE_DIRECTIVE, 
                            RETRIEVAL_INCREMENT_DIRECTIVE,
                            RETRIEVAL_IN_ORDER_DIRECTIVE]

    # List of all supported display directives, i.e. how words are displayed.
    DISPLAY_DIRECTIVES = [DISPLAY_WORD_DIRECTIVE, DISPLAY_SENTENCE_DIRECTIVE]
    
    # Set defaults.
    DEFAULT_RETRIEVAL_DIRECTIVE = RETRIEVAL_IN_ORDER_DIRECTIVE
    DEFAULT_DISPLAY_DIRECTIVE = DISPLAY_WORD_DIRECTIVE
    DEFAULT_DIRECTIVES = [DEFAULT_RETRIEVAL_DIRECTIVE, 
                          DEFAULT_DISPLAY_DIRECTIVE]

    def __init__(self, first_line_in_lesson):       

        """Find directives in first line of lesson, or fall back to defaults.

        First line of lesson is expected to have format <directive, directive>.
        If it doesn't, default directives will be used.

        @param first_line_in_lesson: the top-most line of the lesson file
        @type: first_line_in_lesson: str
        """

        if first_line_in_lesson.find("<") == -1:
            self.__set_default_directives()
            return
        
        directiveMatch = re.search("<(.*)>", first_line_in_lesson)
        if not directiveMatch:
            self.__set_default_directives()
            return

        directiveCommaSeparatedValues = directiveMatch.group(1)
        directiveList = directiveCommaSeparatedValues.split(',')

        retrieval_directive = self.DEFAULT_RETRIEVAL_DIRECTIVE
        display_directive = self.DEFAULT_DISPLAY_DIRECTIVE
        for directive in directiveList:
            directive = directive.strip()
            if directive in self.RETRIEVAL_DIRECTIVES:
                retrieval_directive = directive
            elif directive in self.DISPLAY_DIRECTIVES:
                display_directive = directive

        self.retrieval_directive = retrieval_directive
        self.display_directive = display_directive

    def __set_default_directives(self):

        """Set directives to default values."""

        self.retrieval_directive = self.DEFAULT_RETRIEVAL_DIRECTIVE
        self.display_directive = self.DEFAULT_DISPLAY_DIRECTIVE

    def get_retrieval_directive(self):

        """@rtype: str"""

        return self.retrieval_directive
    
    def get_display_directive(self):

        """@rtype: str"""

        return self.display_directive

