# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'

'''
Decode unicode text to an ASCII representation of the text in Korean.
Based on unidecoder.

'''

import re
from unihandecode.unidecoder import Unidecoder
from unihandecode.krcodepoints import CODEPOINTS as HANCODES
from unihandecode.unicodepoints import CODEPOINTS

class Krdecoder(Unidecoder):
    '''
    example  convert 
    example convert u"내일은 내일 바람이 분다"
    >>> h = Krdecoder()
    >>> print h.decode(u('\ub0b4\uc77c\uc740 \ub0b4\uc77c \ubc14\ub78c\uc774 \ubd84\ub2e4'))
    naeileun naeil barami bunda
    >>> print h.decode(u'(\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f'))
    MyengIlhaMyengIlnoPhwunggaChwiku
    '''

    codepoints = {}

    def __init__(self):
        self.codepoints = CODEPOINTS
        self.codepoints.update(HANCODES)

