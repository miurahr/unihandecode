# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'

'''
Decode unicode text to an ASCII representation of the text in Korean.
Based on unidecoder.

'''

import re
try: #python2
    from cPickle import load
except: #python3
    from pickle import load

from pkg_resources import resource_filename
from unihandecode.unidecoder import Unidecoder

class Krdecoder(Unidecoder):

    codepoints = {}

    def __init__(self):
        unicodepoints_pkl = open(resource_filename(__name__, 'unicodepoints.pickle'), 'rb')
        (self.codepoints, dlen) = load(unicodepoints_pkl)
        dict_pkl = open(resource_filename(__name__, 'krcodepoints.pickle'), 'rb')
        (dic, dlen) = load(dict_pkl)
        self.codepoints.update(dic)

