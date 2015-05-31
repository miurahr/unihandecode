# -*- coding: utf-8 -*-
import unittest
import unihandecode.genkanwadict as genkanwadict

class TestGenkanwadict(unittest.TestCase):
    def constractor(self):
        kanwa = genkanwadict.mkkanwa()
        self.assertEqual(kanwa, object)
