# -*- coding: utf-8 -*-
#  kanwa.py
#
# Copyright 2011 Hiroshi Miura <miurahr@linux.com>
from zlib import decompress
import os
from marshal import loads
try: #python2
    from cPickle import load
    import anydbm as dbm
except: #python3
    from pickle import load
    import dbm as dbm

class kanwa (object):

    _kanwadict = None
    _itaijidict = None
    _jisyo_table = {}

# this class is Borg/Singleton
    _shared_state = {}

    def __new__(cls, *p, **k):
        self = object.__new__(cls, *p, **k)
        self.__dict__ = cls._shared_state
        return self

    def __init__(self):
        if self._kanwadict is None:
            dictpath = os.path.join('unihandecode','pykakasi','kanwadict2')
            self._kanwadict = dbm.open(dictpath,'r')
        if self._itaijidict is None:
            itaijipath = os.path.join('unihandecode','pykakasi','itaijidict2.pickle')
            itaiji_pkl = open(itaijipath, 'rb')
            self._itaijidict = load(itaiji_pkl)

    def haskey(self, key):
        return key in self._itaijidict

    def lookup(self, key):
        return self._itaijidict[key]

    def load(self, char):
        try:#python2
            key = "%04x"%ord(unicode(char))
        except:#python3
            key = "%04x"%ord(char)

        try: #already exist?
            table = self._jisyo_table[key]
        except:
            try:
                table = self._jisyo_table[key]  = loads(decompress(self._kanwadict[key]))
            except:
                return None
        return table
