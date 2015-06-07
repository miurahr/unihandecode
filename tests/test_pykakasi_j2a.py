# -*- coding: utf-8 -*-
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unihandecode.pykakasi.j2a import *

class TestPyKakasiJ2a(unittest.TestCase):
    def test_j2a_canConvert(self):
        k = J2a()
        self.assertTrue(k.canConvert(u'漢'))

    def test_j2a_convert(self):
        k = J2a()
        self.assertEqual(k.convert(u"漢字"), (u"kanji",2))
        self.assertEqual(k.convert(u"森"), (u"mori",1))
        self.assertEqual(k.convert(u"汉"), ("",0))
        self.assertEqual(k.convert(u"a"), ("",0))
