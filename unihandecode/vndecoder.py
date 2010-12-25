# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'

'''
Decode unicode text to an ASCII representation of the text in Vietnamese.

'''

import re
from unidecoder import Unidecoder
from vncodepoints import CODEPOINTS as HANCODES
from unicodepoints import CODEPOINTS

class Vndecoder(Unidecoder):
    '''
    example 
    >>> v = Vndecoder()
    '''

    codepoints = {}

    def __init__(self):
        self.codepoints = CODEPOINTS
        self.codepoints.update(HANCODES)

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()

