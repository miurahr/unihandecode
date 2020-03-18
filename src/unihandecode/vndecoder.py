# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010-2015, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'

'''
Decode unicode text to an ASCII representation of the text in Vietnamese.

'''

from unihandecode.unidecoder import Unidecoder

class Vndecoder(Unidecoder):
    codepoints = {}

    def __init__(self):
        self._load_codepoints('vn')
