# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010-2020 Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'
__all__ = ["Unihandecoder"]

'''
Decode unicode text to an ASCII representation of the text. 
Translate unicode characters to ASCII.

inspired from John's unidecode library.
Copyright(c) 2009, John Schember

Transiliterate the string from unicode characters to ASCII in Chinese and others.
Decode unicode text to an ASCII representation of the text for Japanese.

API is based on the python unidecode,
which is based on Ruby gem (http://rubyforge.org/projects/unidecode/) 
and  perl module Text::Unidecode
(http://search.cpan.org/~sburke/Text-Unidecode-0.04/). 

Copyright (c) 2010,2015,2018,2020 Hiroshi Miura
'''
import os
import pickle
import pkg_resources
import re
from typing import Dict

import unicodedata
import pykakasi  # type: ignore


class Unihandecoder:
    preferred_encoding = None
    decoder = None

    def __init__(self, lang='zh', encoding='utf-8'):
        self.preferred_encoding = encoding
        if lang == "ja":
            self.decoder = Jadecoder()
        elif lang == "kr":
            self.decoder = Krdecoder()
        elif lang == "vn":
            self.decoder = Vndecoder()
        elif lang == "zh":
            self.decoder = Unidecoder('zh')
        else:
            self.decoder = Unidecoder(lang)

    def decode(self, text):
        return self.decoder.decode(unicodedata.normalize('NFC', text))


class Unidecoder:

    codepoints = {}  # type: Dict[str, Dict[int, str]]

    def __init__(self, lang=None):
        self.config = Configurations()
        if lang is not None:
            self._load_codepoints(lang)
        else:
            self._load_codepoints('zh')


    def decode(self, text):
        # Replace characters larger than 127 with their ASCII equivelent.
        return re.sub('[^\x00-\x7f]',lambda x: self.replace_point(x.group()), text)

    def replace_point(self, codepoint):
        '''
        Returns the replacement character or ? if none can be found.
        '''
        try:
            # Split the unicode character xABCD into parts 0xAB and 0xCD.
            # 0xAB represents the group within CODEPOINTS to query and 0xCD
            # represents the position in the list of characters for the group.
            return self.codepoints[self.code_group(codepoint)][self.grouped_point(
                codepoint)]
        except:
            return ''

    def code_group(self, character):
        '''
        Find what group character is a part of.
        '''
        # Code groups withing CODEPOINTS take the form 'xAB'
        return 'x%02x' % (ord(character) >> 8)

    def grouped_point(self, character):
        '''
        Return the location the replacement character is in the list for a
        the group character is a part of.
        '''
        return ord(character) & 255

    def _load_codepoints(self, lang):
        loc_resource = '%scodepoints.pickle' % lang
        for c in ['unicodepoints.pickle', loc_resource]:
            with open(self.config.datapath(c), 'rb') as data:
                (dic, dlen) = pickle.load(data)
                self.codepoints.update(dic)
        return self.codepoints


_unidecoder = None

def unidecode(text):
    global _unidecoder
    if _unidecoder == None:
        _unidecoder = Unihandecoder()
    return _unidecoder.decode(text)


class Jadecoder(Unidecoder):

    def __init__(self):
        super(Jadecoder, self).__init__('ja')
        self.kakasi = pykakasi.kakasi()
        self.kakasi.setMode("J","a")
        self.kakasi.setMode("E","a")
        self.kakasi.setMode("H","a")
        self.kakasi.setMode("K","a")
        self.kakasi.setMode("s", True)
        self.kakasi.setMode("C", True)
        self.conv=self.kakasi.getConverter()

    def decode(self, text):
            result=self.conv.do(text)
            return re.sub('[^\x00-\x7f]', lambda x: self.replace_point(x.group()),result)


class Krdecoder(Unidecoder):

    def __init__(self):
        super(Krdecoder, self).__init__('kr')


class Vndecoder(Unidecoder):

    def __init__(self):
        super(Vndecoder, self).__init__('vn')


# This class is Borg
class Configurations(object):

    _shared_state = {}  # type: Dict[str, object]

    _data_path = pkg_resources.resource_filename(__name__, 'data')

    def __new__(cls, *p, **k):
        self = object.__new__(cls, *p, **k)
        self.__dict__ = cls._shared_state
        return self

    def datapath(self, c: str):
        return os.path.join(self._data_path, c)
