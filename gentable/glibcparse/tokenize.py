#!/usr/bin/env python
# coding=utf8

import re

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from exc import TokenizerError

KEYWORDS = ('LC_IDENTIFICATION', 'LC_CTYPE', 'LC_COLLATE', 'LC_TIME',
            'LC_NUMERIC', 'LC_MONETARY', 'LC_MESSAGES', 'LC_PAPER', 'LC_NAME',
            'LC_ADDRESS', 'LC_TELEPHONE', 'END', 'escape_char', 'comment_char',
            'translit_start', 'translit_end', 'include', 'copy', 'IGNORE',
            'default_missing')

_U_RE = re.compile('<U([0-9A-F]+)>')
def _uni_sub(s):
    def _u_repl(m):
        code_point = int(m.group(1), 16)
        return unichr(code_point)

    return _U_RE.sub(_u_repl, s)

class Tokenizer(object):
    def __init__(self, scrn):
        self.scrn = scrn
        self.word = StringIO()

    @property
    def lineno(self):
        return self.scrn.lineno

    @property
    def colno(self):
        return self.scrn.colno

    @property
    def escape_char(self):
        return self.scrn.escape_char

    @property
    def inside_string(self):
        return self.scrn.inside_string

    @property
    def escaped(self):
        return self.scrn.escaped

    def __iter__(self):
        def _getch():
            c = i.next()
            if self.escape_char == c:
                # drop escape chars
                return _getch()
            return c

        def _reset_word():
            val = self.word.getvalue()
            self.word = StringIO()
            return val

        def _append_char(c):
            self.word.write(c)

        i = iter(self.scrn)
        _reset_word()

        c = _getch()
        while True:
            # non-escaped string start
            if '"' == c and self.inside_string:
                c = _getch()  # skip initial "
                while self.inside_string:
                    if '\n' == c:
                        raise TokenizerError(self, "EOL inside string")

                    _append_char(c)
                    c = _getch()
                c = _getch()  # skip final "
                yield ('STRING', _uni_sub(_reset_word()))
                continue

            # yield EOLs
            if '\n' == c:
                yield ('EOL',)
                c = _getch()
                continue

            # skip whitespace
            if ' ' == c:
                c = _getch()
                continue

            if c == ';':
                yield ('SEMICOLON',)
                c = _getch()
                continue

            if c.isdigit():
                while c.isdigit():
                    _append_char(c)
                    c = _getch()

                yield ('INTEGER', int(_reset_word()))
                continue

            # reads a word
            while self.escaped or c not in (';', ' ', '\n', '"'):
                _append_char(c)
                c = _getch()

            w = _reset_word()
            if w in KEYWORDS:
                yield ('KEYWORD', w)
            else:
                yield ('STRING', _uni_sub(w))
