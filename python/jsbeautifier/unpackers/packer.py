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

import re
from jsbeautifier.unpackers import UnpackingError

PRIORITY = 1

def detect(source):
    return re.match(r'eval *\( *function *\(p, *a, *c, *k, *e, *r',
                     source) is not None

def unpack(source):
    payload, symtab, radix, count = _filterargs(source)

    if radix != 62:
        raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

    if count != len(symtab):
        raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

    def lookup(match):
        word  = match.group(0)
        return symtab[unbase62(word)] or word

    source = re.sub(r'\b\w+\b', lookup, payload)
    return _replacestrings(source)

def _filterargs(source):
    argsregex = r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('\|'\), *(\d+), *(.*)\)\)"
    args = re.search(argsregex, source).groups()
    try:
        return args[0], args[3].split('|'), int(args[1]), int(args[2])
    except ValueError:
        raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

def _replacestrings(source):
    match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source)
    if match:
        varname, strings = match.groups()
        startpoint = len(match.group(0))
        strlist = strings.decode('unicode_escape').split('","')
        lookup = [string.decode('unicode_escape') for string in strlist]
        format = '%s[%%d]' % varname
        for index, var in enumerate(lookup):
            source = source.replace(format % index, '"%s"' % var)
        return source[startpoint:]
    return source

ALPHABET  = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE_DICT = dict((c, i) for i, c in enumerate(ALPHABET))

def unbase62(string):
    ret = 0
    for i, c in enumerate(string[::-1]):
        ret += (62 ** i) * BASE_DICT[c]
    return ret
