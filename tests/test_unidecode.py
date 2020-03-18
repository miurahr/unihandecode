# -*- coding: utf-8 -*-
import sys

import pytest
import unihandecode


def test_unidecode_ascii():
    for n in range(0, 128):
        t = chr(n)
        assert unihandecode.unidecode(t) == t


def test_unidecode_bmp():
    # Just check that it doesn't throw an exception
    for n in range(0, 0x10000):
        t = chr(n)
        unihandecode.unidecode(t)


@pytest.mark.skipif(sys.maxunicode < 0x1d6a4, reason="skip test because of Narrow Python")
def test_unidecode_mathematical_latin():
    # 13 consecutive sequences of A-Z, a-z with some codepoints
    # undefined. We just count the undefined ones and don't check
    # positions.
    empty = 0
    for n in range(0x1d400, 0x1d6a4):
        if n % 52 < 26:
            a = chr(ord('A') + n % 26)
        else:
            a = chr(ord('a') + n % 26)
        b = unihandecode.unidecode(chr(n))
        if not b:
            empty += 1
        else:
            assert b == a
    assert empty == 24


@pytest.mark.skipif(sys.maxunicode < 0x1d800, reason="skip test because of Narrow Python")
def test_unidecode_mathematical_digits():
    # 5 consecutive sequences of 0-9
    for n in range(0x1d7ce, 0x1d800):
        a = chr(ord('0') + (n - 0x1d7ce) % 10)
        b = unihandecode.unidecode(chr(n))
        assert b == a


def test_unidecode_combining_chars():
    TESTS = [("\u0031\u20de", "1")]  # roman number "1" wrapped with solid square
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


def test_unidecode_decomposed_form():
    TESTS = [
        ("\u0041\u0301", "A"),  # "A" with accent mark
        ("\u0061\u0323\u0302", "a"),  # "a" with accent marks
        ("\u30AB\u3099", "ga"),  # "ガ" coded by decomposed from as ' カ゛ '
        ("\u304B\u3099", "ga"),  # "が" coded by decomposed from as ' か゛ '
    ]
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


def test_unidecode_squared_chars():
    TESTS = [
        ("\u3301", "alpha"),  # combined Alpha in Katakana
        ("\u3302", "ampere"),  # combined Ampere in Katakana
        ("\u3304", "inning"),
        ("\u3306", "won"),  # combined Won in Katakana
        ("\u3307", "escudo"),
        ("\u3308", "acre"),  # combined Acre in Katakana
        ("\u3309", "ounce"),  # combined ounce in Katakana
        ("\u330a", "ohm"),  # combined Ohm in Katakana
        ("\u3349", "milli"),  # milli in Katakana
        ("\u3314", "kilo"),  # kilo in Katakana
        ("\u3315", "kilogram"),  # kilo gram in Katakana
        ("\u3316", "kilometer"),  # kilo metre in Katakana
        ("\u3322", "centi"),  # centi in Katakana
        ("\u334d", "meter"),  # metre in Katakana
        ("\u3318", "gram"),  # gram in Katakana
        ("\u3327", "ton"),  # ton in Katakana
        ("\u3303", "are"),  # are in Katakana
        ("\u3336", "hectare"),  # hect-are in Katakana
        ("\u337f", "Inc."),  # kabusiki kaisha in Katakana
    ]
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


def test_unidecode_compatibility_composite():
    TESTS = [
        ("\ufb01", "fi"),
        ("\u0032\u2075", "25"),
    ]
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


def test_unidecode_mac_japanese_pua():
    TESTS = [
        ("\uF862\u6709\u9650\u4F1A\u793E",  # Adobe CID 8321
         "You Xian Hui She "),  # "yuugengaisha" in unihandecode(ja)
        ("\u5927\u20dd", "Da "),  # "大" with circle "Dai " in unihandecode(ja)
        ("\u5c0f\u20dd", "Xiao "),  # "小" with circle "Shou " in unihandecode(ja)
        ("\u63a7\u20dd", "Kong "),  # "控" with circle "Hikae " in unihandecode(ja)
    ]
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


def test_unidecode_specific_bmp():
    TESTS = [
        ("Hello, World!", "Hello, World!"),
        ("'\"\r\n", "'\"\r\n"),
        ("ČŽŠčžš", "CZSczs"),
        ("\u00a0\u00a1\u00a2\u00a3\u00a4\u00a5\u00a6\u00a7", " !C/PS\u005c$?Y=|SS"),
        ("\u00a8\u00a9\u00aa\u00ab\u00ac\u00ad\u00ae\u00af", "\u0022(c)a<<!(r)-"),
        ("ア", "a"),
        ("α", "a"),
        ("а", "a"),
        ('ch\xe2teau', "chateau"),
        ('vi\xf1edos', "vinedos"),
        ("\u5317\u4EB0", "Bei Jing "),
        ("Efﬁcient", "Efficient"),
        # Table that doesn't exist
        ('\ua500', ''),
        # Table that has less than 256 entriees
        ('\u1eff', ''),
        # Mark area
        ("\u210a", "g"),  # gram mark
    ]
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


@pytest.mark.skipif(sys.maxunicode < 0x1d6a4, reason="skip test because of Narrow Python")
def test_unidecode_specific_supplementary():
    TESTS = [
        ('\U0001d5a0', 'A'),  # Non-BMP character
        ('\U0001d5c4\U0001d5c6/\U0001d5c1', 'km/h'),  # Mathematical
    ]
    for input, output in TESTS:
        assert unihandecode.unidecode(input) == output


def test_unidecode_kana():
    for n in range(0x3000, 0x30ff):
        # Just check that it doesn't throw an exception
        t = chr(n)
        unihandecode.unidecode(t)


def test_unidecode_zh():
    ZHTESTS = [
        ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439", 'Ming Tian Ming Tian De Feng Chui '),
        ("馮", "Feng "),
    ]
    for input, output in ZHTESTS:
        assert unihandecode.unidecode(input) == output
