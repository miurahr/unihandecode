#!/usr/bin/env python
# coding=utf8

import re

PREFACE_RE = re.compile(
    '^(\s*(?:escape_char|comment_char)\s*.\s*\n)*'
)

def strip_comments(comment_char, escape_char, string_delim, i):
    inside_string = False
    escaped = False

    # remove comments
    while True:
        c = i.next()

        if escaped:
            escaped = False
            yield c
            continue

        if escape_char == c:
            escaped = True
        elif string_delim == c:
            inside_string = not inside_string
        elif comment_char == c and not inside_string:
            while c != '\n':
                c = i.next()

        yield c


def preprocess(buf):
    preface_m = PREFACE_RE.search(buf)

    escape_char = '\\'
    comment_char = '#'
    string_delim = '"'

    if preface_m:
        for line in preface_m.group(0).split('\n'):
            # skip blank lines
            if not line:
                continue

            cmd, ch = line.strip().split()

            if cmd == 'escape_char':
                escape_char = ch
            elif cmd == 'comment_char':
                comment_char = ch

        # start reading after preface
        i = iter(buffer(buf, preface_m.end()))
    else:
        i = iter(buf)

    return escape_char,\
           string_delim,\
           strip_comments(comment_char,
                          escape_char,
                          string_delim,
                          i)


class Screener(object):
    def __init__(self, buf):
        self.escape_char, self.string_delim, self.i = preprocess(buf)
        self.lineno = 0
        self.colno = 0
        self.inside_string = False
        self._newline = False
        self.escaped = False

    def __iter__(self):
        def _getch():
            if self._newline:
                self.lineno += 1
                self.colno = 0
                self._newline = False
            else:
                self.colno += 1

            c = self.i.next()
            if '\n' == c:
                self._newline = True
            return c

        # skip initial whitespace
        c = _getch()
        while c.isspace():
            c = _getch()

        while True:
            if self.escaped:
                if '\n' != c:
                    # escaped newlines simply disappear
                    yield self.escape_char
                    yield c
                c = _getch()
                self.escaped = False
                continue

            # not escaped:
            if self.escape_char == c:
                self.escaped = True
                c = _getch()
                continue
            elif self.string_delim == c:
                self.inside_string = not self.inside_string
                c = _getch()
                yield self.string_delim
                continue
            if not self.inside_string:
                if '\n' == c:
                    # compact newlines
                    while '\n' == c:
                        c = _getch()
                    yield '\n'
                    continue
                elif c.isspace():
                    while c.isspace() and c != '\n':
                        c = _getch()
                    yield ' '
                    continue

            yield c
            c = _getch()
            continue
