# -*- coding: utf-8 -*-
from unihandecode import Unidecoder


def test_code_group():
    assert Unidecoder('zh').code_group("\u1234") == 'x12'


def test_grouped_point():
    assert Unidecoder('zh').grouped_point("\u1234") == 0x34


def test_decode():
    assert Unidecoder('zh').decode("a") == "a"


def test_replace_point():
    assert Unidecoder('zh').replace_point('a') == 'a'
