# -*- coding: utf-8 -*-
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unihandecode.pykakasi.itaiji import itaiji

class TestItaiji(unittest.TestCase):
    def test_itaiji_haskey(self):
        k = itaiji()
        self.assertTrue(k.haskey(u'壱'))

    def test_itaiji_lookup(self):
        k = itaiji()
        self.assertEqual(k.lookup(u'壱'), u'一')

    def test_itaiji_canConvert(self):
        k = itaiji()
        self.assertTrue(k.canConvert(u'壱'))

    def test_itaiji_convert(self):
        k = itaiji()
        self.assertEqual(k.convert(u"壱弍"),u"一二")

