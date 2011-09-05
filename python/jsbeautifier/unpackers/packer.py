#
# Unpacker for Dean Edward's p.a.c.k.e.r, a part of javascript beautifier
# by Einar Lielmanis <einar@jsbeautifier.org>
#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#
# usage:
#
# if detect(some_string):
#     unpacked = unpack(some_string)
#

"""Unpacker for Dean Edward's p.a.c.k.e.r"""

import re
from jsbeautifier.unpackers import UnpackingError

PRIORITY = 1

def detect(source):
    """Detects whether `source` is P.A.C.K.E.R. coded."""
    return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,r')

def unpack(source):
    """Unpacks P.A.C.K.E.R. packed js code."""
    payload, symtab, radix, count = _filterargs(source)

    if radix != 62:
        raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

    if count != len(symtab):
        raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

    def lookup(match):
        """Look up symbols in the synthetic symtab."""
        word  = match.group(0)
        return symtab[unbase62(word)] or word

    source = re.sub(r'\b\w+\b', lookup, payload)
    return _replacestrings(source)

def _filterargs(source):
    """Juice from a source file the four args needed by decoder."""
    argsregex = (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\."
                 r"split\('\|'\), *(\d+), *(.*)\)\)")
    args = re.search(argsregex, source).groups()
    try:
        return args[0], args[3].split('|'), int(args[1]), int(args[2])
    except ValueError:
        raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

def _replacestrings(source):
    """Strip string lookup table (list) and replace values in source."""
    match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source)
    if match:
        varname, strings = match.groups()
        startpoint = len(match.group(0))
        lookup = strings.split('","')
        variable = '%s[%%d]' % varname
        for index, value in enumerate(lookup):
            source = source.replace(variable % index, '"%s"' % value)
        return source[startpoint:]
    return source

ALPHABET  = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE_DICT = dict((cipher, index) for index, cipher in enumerate(ALPHABET))

def unbase62(string):
    """Decodes a base62 value to an integer."""
    ret = 0
    for index, cipher in enumerate(string[::-1]):
        ret += (62 ** index) * BASE_DICT[cipher]
    return ret
