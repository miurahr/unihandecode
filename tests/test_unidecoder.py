# -*- coding: utf-8 -*-
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from unihandecode.unidecoder import Unidecoder

class TestUnidecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = Unidecoder('zh')

    def test_code_group(self):
        self.assertEqual(self.decoder.code_group(u"\u1234"), 'x12')

    def test_grouped_point(self):
        self.assertEqual(self.decoder.grouped_point(u"\u1234"), 0x34)

    def test_decode(self):
        self.assertEqual(self.decoder.decode("a"), "a")

    def test_replace_point(self):
        self.assertEqual(self.decoder.replace_point('a'),'a')
