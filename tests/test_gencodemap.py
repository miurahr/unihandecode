# -*- coding: utf-8 -*-
import os,sys,bz2
import unihandecode.gencodemap as gencodemap
from types import *
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
try: #python2
    import cPickle as pickle
except: #python3
    import pickle
import tempfile
import shutil

class TestGencodemap(unittest.TestCase):

    def setUp(self):
        self.workspace = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workspace)

    def test_default_lang(self):
        u = gencodemap.UnihanConv('ru')
        self.assertTrue(isinstance(u ,gencodemap.UnihanConv))

    def test_checkcategory(self):
        u = gencodemap.UnihanConv('zh')
        u.check_category("key",'kHanyuPinyin', u"10038.080:yǐn")

    def test_gencodemap(self):
        unihan_source = os.path.join('unihandecode','data','Unihan_Readings.txt')
        dest = os.path.join(self.workspace,'krcodepoints.pickle')
        u = gencodemap.UnihanConv('kr')
        u.run(source = unihan_source, dest=dest)

        f = open(os.path.join(self.workspace, 'krcodepoints.pickle.bz2'),'rb')
        buf = f.read()
        buf = bz2.decompress(buf)
        (dic, dlen) = pickle.loads(buf)
        self.assertTrue(isinstance(dic, dict))

    def test_unicodepoints(self):
         # build unicode maps
        u = gencodemap.Unicodepoints()
        u.run(os.path.join(self.workspace,'unicodepoints.pickle'))

        f = open(os.path.join(self.workspace, 'unicodepoints.pickle.bz2'),'rb')
        buf = f.read()
        buf = bz2.decompress(buf)
        (dic, dlen) = pickle.loads(buf)
        self.assertTrue(isinstance(dic, dict))
