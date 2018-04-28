# coding:utf8
__license__ = 'GPL 3'
__copyright__ = '2010-2018, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'

'''
Decode unicode text to an ASCII representation of the text for Japanese.
 Translate unicode string to ASCII roman string.

API is based on the python unidecode,
which is based on Ruby gem (http://rubyforge.org/projects/unidecode/) 
and  perl module Text::Unidecode
(http://search.cpan.org/~sburke/Text-Unidecode-0.04/). 

This functionality is owned by Kakasi Japanese processing engine.

Copyright (c) 2010,2015,2018 Hiroshi Miura
'''

import os,re

from unihandecode.unidecoder import Unidecoder
import pykakasi

class Jadecoder(Unidecoder):
    kakasi = None
    codepoints = {}

    def __init__(self):
        self._load_codepoints('ja')
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

