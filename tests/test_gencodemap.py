# -*- coding: utf-8 -*-
import os
import pickle

import unihandecode.gencodemap as gencodemap


def test_default_lang():
    u = gencodemap.UnihanConv('ru')
    assert isinstance(u, gencodemap.UnihanConv)


def test_checkcategory():
    u = gencodemap.UnihanConv('zh')
    u.check_category("key", 'kHanyuPinyin', u"10038.080:yǐn")


def test_gencodemap(tmp_path):
    rootdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    unihan_source = os.path.join(rootdir, 'src', 'unihandecode', 'data', 'Unihan_Readings.txt')
    dest = os.path.join(tmp_path, 'krcodepoints.pickle')
    u = gencodemap.UnihanConv('kr')
    u.run(source=unihan_source, dest=dest)
    with open(os.path.join(tmp_path, 'krcodepoints.pickle'), 'rb') as f:
        (dic, dlen) = pickle.load(f)
        assert isinstance(dic, dict)


def test_unicodepoints(tmp_path):
    # build unicode maps
    u = gencodemap.Unicodepoints()
    u.run(os.path.join(tmp_path, 'unicodepoints.pickle'))

    with open(os.path.join(tmp_path, 'unicodepoints.pickle'), 'rb') as f:
        (dic, dlen) = pickle.load(f)
        assert isinstance(dic, dict)
