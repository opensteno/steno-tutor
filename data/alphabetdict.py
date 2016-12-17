# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""
Steno to steno mapping...for example, a "B" on the left of a steno
keyboard will map to steno keys PW, whereas on the right it is B. 
"""

STENO_ALPHABET = {
    'A' : 'A',
    'B' : 'PW',
    '-B' : '-B',
    'C': 'KR',
    'D': 'TK',
    '-D': '-D',
    'E': 'E',
    'F': 'TP',
    '-F': '-F',
    'G': 'TKPW',
    '-G': '-G',
    'H': 'H',
    'I': 'EU',
    'J': 'SKWR',
    '-J': '-PBLG',
    'K': 'K',
    '-K': '-BG',
    'L': 'HR',
    '-L': '-L',
    'M': 'PH',
    '-M': '-PL',
    'N': 'TPH',
    '-N': '-PB',
    'O': 'O',
    'P': 'P',
    '-P': '-P',
    'Q': 'KW',
    'R': 'R',
    '-R': '-R',
    'S': 'S',
    '-S': '-S',
    'T': 'T',
    '-T': '-T',
    'U': 'U',
    'V': 'SR',
    '-V': '-F',
    'W': 'W',
    'X': 'KP',
    '-X': '-BGS',
    'Y': 'KWR',
    'Z': 'STKPW',
    '-Z': '-Z',
    '*': '*'}

INVERSE_STENO = dict((v,k) for k, v in STENO_ALPHABET.iteritems())

