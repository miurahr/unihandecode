import os

import pytest

import unihandecode.gencodemap as gencodemap

datadir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'unihandecode', 'data', 'transforms')


@pytest.mark.parametrize("lang, file, key, expected", [
    ('am', 'Amharic-Latin-BGN.xml', 'ከ', 'ke'),
    ('bengali', 'Bengali-InterIndic.xml', 'ো', "\uE04B")
])
def test_trule_get_rule_source(lang, file, key, expected):
    transform_rule = gencodemap.TransformRule(lang)
    transform_rule.load(os.path.join(datadir, file))
    tbl = transform_rule.as_dictionary()
    assert tbl is not None
    assert len(tbl) > 0
    assert tbl[key] == expected
