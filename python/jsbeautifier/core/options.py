# The MIT License (MIT)
#
# Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy

# merges child options up with the parent options object
# Example: obj = {a: 1, b: {a: 2}}
#          mergeOpts(obj, 'b')
#
#          Returns: {a: 2, b: {a: 2}}


def mergeOpts(options, childFieldName):
    finalOpts = copy.copy(options)

    local = getattr(finalOpts, childFieldName, None)
    if local:
        delattr(finalOpts, childFieldName)
        for key in local:
            setattr(finalOpts, key, local[key])

    return finalOpts

def normalizeOpts(options):
    convertedOpts = copy.copy(options)

    for key in options.__dict__:
        if '-' in key:
            delattr(convertedOpts, key)
            setattr(convertedOpts, key.replace('-', '_'), getattr(options, key, None))

    return convertedOpts
