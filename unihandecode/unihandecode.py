# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'

'''
Decode unicode text to an ASCII representation of the text. 
Translate unicode characters to ASCII.

inspired from John's unidecode library.
Copyright(c) 2009, John Schember

Tranliterate the string from unicode characters to ASCII in Chinese and others.

example  convert:  "明天明天的风吹", "明日は明日の風が吹く" and "내일은 내일 바람이 분다"
>>> d = Unihandecoder("utf-8")
>>> print d.decode(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439", lang="ch")
Ming Tian Ming Tian De Feng Chui 
>>> print d.decode(u'\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f', lang="ja")
Ashita ha Ashita no Kaze ga Fuku
'''

from unidecoder import Unidecoder
from kandecoder import Kandecoder
from handecoder import Handecoder

class Unihandecoder(object):
    preferred_encoding = None
    lang = None

    def __init__(self, encoding='utf-8', lang="ch"):
        self.preferred_encoding = encoding
        self.lang = lang

    def decode(self, text):

        if not isinstance(text, unicode):
            try:
                text = unicode(text)
            except:
                try:
                    text = text.decode(self.preferred_encoding)
                except:
                    text = text.decode('utf-8', 'replace')

        if self.lang is "ja":
            d = Kandecoder()
            return d.decode(text)
        elif self.lang is "kr":
            d = Handecoder()
            return d.decode(text)
        else:
            d = Unidecoder()
            return d.decode(text)

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()

