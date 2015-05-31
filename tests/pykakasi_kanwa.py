# -*- coding: utf-8 -*-
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import unihandecode.genkanwadict as genkanwadict

class TestGenkanwadict(unittest.TestCase):
    def constractor(self):
        kanwa = genkanwadict.mkkanwa()
        self.assertEqual(kanwa, object)
