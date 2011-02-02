# -*- coding: utf-8 -*-
#  jisyo.py
#
# Copyright 2011 Hiroshi Miura <miurahr@linux.com>
from zlib import decompress
import os,marshal
try: #python2
    from cPickle import load
    import anydbm as dbm
except: #python3
    from pickle import load
    import dbm as dbm

class jisyo (object):

    _kanwadict = None
    _itaijidict = None
    _kanadict = None
    _jisyo_table = {}

# this class is Borg/Singleton
    _shared_state = {}

    def __new__(cls, *p, **k):
        self = object.__new__(cls, *p, **k)
        self.__dict__ = cls._shared_state
        return self

    def __init__(self):
        if self._kanwadict is None:
            dictpath = os.path.join('unihandecode','pykakasi','kanwadict2.db')
            self._kanwadict = dbm.open(dictpath,'r')
        if self._itaijidict is None:
            itaijipath = os.path.join('unihandecode','pykakasi','itaijidict2.pickle')
            itaiji_pkl = open(itaijipath, 'rb')
            self._itaijidict = load(itaiji_pkl)
        if self._kanadict is None:
            kanadictpath = os.path.join('unihandecode','pykakasi','kanadict2.pickle')
            kanadict_pkl = open(kanadictpath, 'rb')
            self._kanadict = load(kanadict_pkl)

    def kana_haskey(self, key):
        return key in self._kanadict

    def kana_lookup(self,key):
        return self._kanadict[key]

    def itaiji_haskey(self, key):
        return key in self._itaijidict

    def itaiji_lookup(self, key):
        return self._itaijidict[key]

    def load_jisyo(self, char):
        try:#python2
            key = "%04x"%ord(unicode(char))
        except:#python3
            key = "%04x"%ord(char)

        try: #already exist?
            table = self._jisyo_table[key]
        except:
            try:
                table = self._jisyo_table[key]  = marshal.loads(decompress(self._kanwadict[key]))
            except:
                return None
        return table

