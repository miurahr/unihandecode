#!/usr/bin/env python
# coding=utf8


class LException(Exception):
    def __init__(self, src, err):
        super(LException, self).__init__(err)

        self.src = src
        self.err = err


class TokenizerError(LException):
    pass


class ParserError(LException):
    pass
