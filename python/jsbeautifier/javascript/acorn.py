# This is done due to the build system being how it is
try:
    re = __import__("regex")
except ImportError:
    import re

# This section of code was translated to python from acorn (javascript).
#
# Acorn was written by Marijn Haverbeke and released under an MIT
# license. The Unicode regexps (for identifiers and whitespace) were
# taken from [Esprima](http://esprima.org) by Ariya Hidayat.
#
# Git repositories for Acorn are available at
#
#     http://marijnhaverbeke.nl/git/acorn
#     https://github.com/marijnh/acorn.git

# ## Character categories

# acorn used char codes to squeeze the last bit of performance out
# Beautifier is okay without that, so we're using regex
# permit #(23), $ (36), and @ (64). @ is used in ES7 decorators.
# 65 through 91 are uppercase letters.
# permit _ (95).
# 97 through 123 are lowercase letters.
_baseASCIIidentifierStartChars = r"\x23\x24\x40\x41-\x5a\x5f\x61-\x7a"

# inside an identifier @ is not allowed but 0-9 are.
_baseASCIIidentifierChars = r"\x24\x30-\x39\x41-\x5a\x5f\x61-\x7a"

# Regular expressions that match characters in the whitespace,
# identifier, and identifier-start categories. These are only
# applied when a character is found to actually have a code point
# above 128. Hopefully this properly matches the full identifier
# specification, but if not it at least doesn't break any tests
# and does fix some cases.
_nonASCIIidentifierStartChars = r"\p{L}\p{Nl}"
_nonASCIIidentifierChars = r"\p{L}\p{Nl}\p{Nd}\p{Pc}\p{Mn}\p{Mc}"

# _nonASCIIidentifierStart = re.compile("[" + _nonASCIIidentifierStartChars + "]")
# _nonASCIIidentifier = re.compile("[" + _nonASCIIidentifierStartChars + _nonASCIIidentifierChars + "]")

_unicodeEscapeOrCodePoint = r"\\u[0-9a-fA-F]{4}|\\u\{[0-9a-fA-F]+\}"

_identifierStart = (
    "(?:"
    + _unicodeEscapeOrCodePoint
    + "|["
    + _baseASCIIidentifierStartChars
    + _nonASCIIidentifierStartChars
    + "])"
)
_identifierChars = (
    "(?:"
    + _unicodeEscapeOrCodePoint
    + "|["
    + _baseASCIIidentifierChars
    + _nonASCIIidentifierStartChars
    + _nonASCIIidentifierChars
    + "])*"
)

identifier = re.compile(_identifierStart + _identifierChars)

identifierStart = re.compile(_identifierStart)
identifierMatch = re.compile(
    "(?:"
    + _unicodeEscapeOrCodePoint
    + "|["
    + _baseASCIIidentifierChars
    + _nonASCIIidentifierStartChars
    + _nonASCIIidentifierChars
    + "])+"
)

_nonASCIIwhitespace = re.compile(r"[\u1680\u180e\u2000-\u200a\u202f\u205f\u3000\ufeff]")

# Whether a single character denotes a newline.
newline = re.compile(r"[\n\r\u2028\u2029]")

# Matches a whole line break (where CRLF is considered a single
# line break). Used to count lines.

# in javascript, these two differ
# in python they are the same, different methods are called on them
lineBreak = re.compile(r"\r\n|[\n\r\u2028\u2029]")
allLineBreaks = lineBreak
