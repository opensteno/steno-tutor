# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Loads dictionaries that have been pickled in json."""

import json

ALTERNATIVE_ENCODING = 'latin-1' 


def load_dict(dictionary_filename):

    """Load json dict with file name provided.

    @param dictionary_filename: path to an existing json dict
    @type dictionary_filename: str

    @return: dictionary in file
    @rtype: dict
    """

    try:
        with open(dictionary_filename, 'r') as f:
            dictionary = json.load(f)

    except UnicodeDecodeError:
        with open(dictionary_filename, 'r') as f:
            dictionary = json.load(f, ALTERNATIVE_ENCODING)

    return dictionary


