# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Steno to qwerty mappings."""


QWERTY_TO_STENO_KEYS = {
    'Q':'S',
    'W':'T',
    'E':'P',
    'R':'H',
    'T':'*',
    'Y':'*',
    'U':'-F',
    'I':'-P',
    'O':'-L',
    'P':'-T',
    '[':'-D',
    'A':'S',
    'S':'K',
    'D':'W',
    'F':'R',
    'G':'*',
    'H':'*',
    'J':'-R',
    'K':'-B',
    'L':'-G',
    ';':'-S',
    '\'':'-Z',
    'C':'A',
    'V':'O',
    'N':'E',
    'M':'U'
}

QWERTY_COMBO_STENO_LETTERS = [
    ('QWEASD', 'Z'),
    ('WSED','G'),
    ('QASDF', 'J'),
    ('IOKL', 'J'),
    ('WER', 'N'),
    ('SDF', 'Y'),
    ('KL;', 'X'),
    ('QAF', 'V'),
    ('QA','S'),
    ('ED','B'),
    ('WS', 'D'),
    ('WE', 'F'),
    ('KL', 'K'),
    ('RF', 'L'),
    ('ER', 'M'),
    ('IO', 'M'),
    ('IK', 'N'),
    ('SE', 'X'),
    ('SF', 'C'),
    ('NM', 'I'),
    ('SD', 'Q'),
    ('U', 'V'),
]


STENO_TO_QWERTY = {
    '-D': '[',
    '-G': 'L',
    '-F': 'U', 
    '-B': 'K', 
    '-L': 'O', 
    '-T': 'P', 
    '-P': 'I', 
    '-S': ';', 
    '-R': 'J', 
    '-Z': "'", 
    '*': 'TYGH', 
    'A': 'C', 
    'E': 'N', 
    'H': 'R', 
    'K': 'S',
    'O': 'V', 
    'P': 'E', 
    'S': 'QA', 
    'R': 'F', 
    'U': 'M', 
    'T': 'W', 
    'W': 'D'
}


