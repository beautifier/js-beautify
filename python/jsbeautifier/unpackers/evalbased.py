#
# Unpacker for eval() based packers, a part of javascript beautifier
# by Einar Lielmanis <einar@jsbeautifier.org>
#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#
# usage:
#
# if detect(some_string):
#     unpacked = unpack(some_string)
#

PRIORITY = 3

def detect(source):
    return source.strip().lower().startswith('eval(function(')

def unpack(source):
    return js('print %s;' % source[4:]) if detect(source) else source

# In case of failure, we'll just return the original, without crashing on user.
def js(script):
    from subprocess import PIPE, Popen
    try:
        interpreter = Popen(['js'], stdin=PIPE, stdout=PIPE)
    except OSError:
        return script
    result, errors = interpreter.communicate(script)
    if interpreter.poll() or errors:
        return script
    return result
