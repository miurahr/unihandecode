# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'
__all__ = ["Unihandecoder"]

'''
Decode unicode text to an ASCII representation of the text. 
Translate unicode characters to ASCII.

inspired from John's unidecode library.
Copyright(c) 2009, John Schember

Tranliterate the string from unicode characters to ASCII in Chinese and others.

'''

from unihandecode.unidecoder import Unidecoder
from unihandecode.jadecoder import Jadecoder
from unihandecode.krdecoder import Krdecoder
from unihandecode.vndecoder import Vndecoder

#python 2,3 compatibility
try:
    unicode # python2
    def u(str): return str.decode("utf-8")
    pass
except: #python 3
    def u(str): return str
    pass

class Unihandecoder(object):
    preferred_encoding = None
    lang = None

    def __init__(self, lang="zh", encoding='utf-8'):
        self.preferred_encoding = encoding
        self.lang = lang

    def decode(self, text):
        '''
        example  convert:  "明天明天的风吹", "明日は明日の風が吹く" 
          and "내일은 내일 바람이 분다"
        >>> d = Unihandecoder(lang="zh")
        >>> print d.decode(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439")
        Ming Tian Ming Tian De Feng Chui 
        >>> d = Unihandecoder(lang="ja")
        >>> print d.decode(u'\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f')
        Ashita ha Ashita no Kaze ga Fuku
        >>> d = Unihandecoder(lang="kr")
        >>> print d.decode(u'\ub0b4\uc77c\uc740 \ub0b4\uc77c \ubc14\ub78c\uc774 \ubd84\ub2e4')
        naeileun naeil barami bunda

        '''

        try:
            unicode # python2
            if not isinstance(text, unicode):
                try:
                    text = unicode(text)
                except:
                    try:
                        text = text.decode(self.preferred_encoding)
                    except:
                        text = text.decode('utf-8', 'replace')
        except: # python3, str is unicode
            pass

        if self.lang is "ja":
            d = Jadecoder()
            return d.decode(text)
        elif self.lang is "kr":
            d = Krdecoder()
            return d.decode(text)
        elif self.lang is "vn":
            d = Vndecoder()
            return d.decode(text)
        else: #zh and others
            d = Unidecoder()
            return d.decode(text)

