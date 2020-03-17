# -*- coding: utf-8 -*-
import bz2
import os
import unihandecode.gencodemap as gencodemap
import pickle

def test_default_lang():
    u = gencodemap.UnihanConv('ru')
    assert isinstance(u ,gencodemap.UnihanConv)


def test_checkcategory():
    u = gencodemap.UnihanConv('zh')
    u.check_category("key",'kHanyuPinyin', u"10038.080:yǐn")


def test_gencodemap(tmp_path):
    unihan_source = os.path.join('unihandecode','data','Unihan_Readings.txt')
    dest = os.path.join(tmp_path,'krcodepoints.pickle')
    u = gencodemap.UnihanConv('kr')
    u.run(source = unihan_source, dest=dest)
    f = open(os.path.join(tmp_path, 'krcodepoints.pickle.bz2'),'rb')
    buf = f.read()
    buf = bz2.decompress(buf)
    (dic, dlen) = pickle.loads(buf)
    assert isinstance(dic, dict)


def test_unicodepoints(tmp_path):
     # build unicode maps
    u = gencodemap.Unicodepoints()
    u.run(os.path.join(tmp_path,'unicodepoints.pickle'))

    f = open(os.path.join(tmp_path, 'unicodepoints.pickle.bz2'),'rb')
    buf = f.read()
    buf = bz2.decompress(buf)
    (dic, dlen) = pickle.loads(buf)
    assert isinstance(dic, dict)
