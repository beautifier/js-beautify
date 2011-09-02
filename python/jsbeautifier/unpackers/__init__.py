#
# General code for JSBeautifier unpackers infrastructure. See README.specs
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

class UnpackingError(Exception):
    pass

def getunpackers():
    import pkgutil
    path = __path__
    prefix = __name__ + '.'
    unpackers = []
    interface = ['unpack', 'detect', 'PRIORITY']
    for importer, modname, ispkg in pkgutil.iter_modules(path, prefix): #onerror
        if 'tests' not in modname:
            try:
                module = __import__(modname, fromlist=interface)
            except ImportError:
                raise UnpackingError('Bad unpacker: %s' % modname)
            else:
                unpackers.append(module)

    return sorted(unpackers, key = lambda mod: mod.PRIORITY)

_unpackers = getunpackers()

def run(source):
    for unpacker in [mod for mod in _unpackers if mod.detect(source)]:
        source = unpacker.unpack(source)
    return source

# TODO see if necessary
def filtercomments(source):
    import re

    trailing_comments = []
    comment = True

    while comment:
        if re.search(r'^\s*\/\*', source):
            comment = source[0, source.index('*/') + 2]
        elif re.search(r'^\s*\/\/', source):
            comment = re.search(r'^\s*\/\/', source).group(0)
        else:
            comment = None

        if comment:
            source = re.sub(r'^\s+', '', source[len(comment):])
            trailing_comments.append(comment)

    return '\n'.join(trailing_comments) + source
