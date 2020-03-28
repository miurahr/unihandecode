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
from typing import Dict, Optional

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


class CodePoints:

    def __init__(self, lang='zh'):
        self.config = Configurations()
        self.codepoints = {}  # type: Dict[int, Optional[str]]
        for c in ['unicodepoints.pickle', '%scodepoints.pickle' % lang]:
            with open(self.config.datapath(c), 'rb') as data:
                dic = pickle.load(data)
                self.codepoints.update(dic)

    def __getitem__(self, item):
        try:
            return self.codepoints[item]
        except LookupError:
            return None


class Unidecoder:

    def __init__(self, lang='zh'):
        self.codepoints = CodePoints(lang)

    def decode(self, text):
        return text.translate(self.codepoints)


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
            return result.translate(self.codepoints)


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
