import sys

import pytest
from unihandecode import Unihandecoder


def test_ascii():
    u = Unihandecoder(lang="zh")
    for n in range(0, 128):
        t = chr(n)
        assert u.decode(t) == t


def test_bmp():
    u = Unihandecoder(lang="zh")
    for n in range(0, 0x10000):
        # Just check that it doesn't throw an exception
        t = chr(n)
        u.decode(t)


@pytest.mark.skipif(sys.maxunicode < 0x1d6a4, reason="skip test because of Narrow Python")
def test_mathematical_latin():
    # 13 consecutive sequences of A-Z, a-z with some codepoints
    # undefined. We just count the undefined ones and don't check
    # positions.
    empty = 0
    u = Unihandecoder(lang="zh")
    for n in range(0x1d400, 0x1d6a4):
        if n % 52 < 26:
            a = chr(ord('A') + n % 26)
        else:
            a = chr(ord('a') + n % 26)
        b = u.decode(chr(n))

        if not b:
            empty += 1
        else:
            assert b == a
    assert empty == 24


@pytest.mark.skipif(sys.maxunicode < 0x1d800, reason="skip test because of Narrow Python")
def test_mathematical_digits():
    u = Unihandecoder(lang="zh")
    # 5 consecutive sequences of 0-9
    for n in range(0x1d7ce, 0x1d800):
        a = chr(ord('0') + (n - 0x1d7ce) % 10)
        b = u.decode(chr(n))
        assert b == a


@pytest.mark.parametrize("case, expected", [
    ("\u30AB\u3099", "ga"),  # "ガ" coded by decomposed from as ' カ゛ '
    ("\u304B\u3099", "ga"),  # "が" coded by decomposed from as ' か゛ '
])
def test_decomposed_form(case, expected):
    u = Unihandecoder(lang="ja")
    assert u.decode(case) == expected


@pytest.mark.parametrize("case, expected", [
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
])
def test_squared_chars(case, expected):
    u = Unihandecoder(lang="ja")
    assert u.decode(case) == expected


@pytest.mark.parametrize("case, expected", [
    ("\ufb01", "fi"),
    ("\u0032\u2075", "25"),
    ("\u0041\u0301", "A"),  # "A" with accent mark
    ("\u0061\u0323\u0302", "a"),  # "a" with accent marks
    ("\u0031\u20de", "1"),  # roman number "1"  wrapped with solid square
])
def test_compatibility_composite(case, expected):
    u = Unihandecoder(lang="zh")
    assert u.decode(case) == expected


@pytest.mark.parametrize("case, expected", [
    ("\uF862\u6709\u9650\u4F1A\u793E",  # Adobe CID 8321
     "Yuugengaisha"),
    ("\u5927\u20dd", "Dai "),  # "大" with circle
    ("\u5c0f\u20dd", "Shou "),  # "小" with circle
    ("\u63a7\u20dd", "Hikae "),  # "控" with circle
])
def test_mac_japanese_pua(case, expected):
    assert Unihandecoder(lang="ja").decode(case) == expected


@pytest.mark.parametrize("case, expected", [
    ("Hello, World!", "Hello, World!"),
    ("'\"\r\n", "'\"\r\n"),
    ("ČŽŠčžš", "CZSczs"),
    ("\u00a0\u00a1\u00a2\u00a3\u00a4\u00a5\u00a6\u00a7", " !C/PS$?Y=|SS"),
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
])
def test_specific_bmp(case, expected):
    assert Unihandecoder(lang="zh").decode(case) == expected


@pytest.mark.skipif(sys.maxunicode < 0x1d6a4, reason="skip test because of Narrow Python")
@pytest.mark.parametrize("case, expected", [
    ('\U0001d5a0', 'A'),  # Non-BMP character
    ('\U0001d5c4\U0001d5c6/\U0001d5c1', 'km/h'),  # Mathematical
])
def test_specific_supplementary(case, expected):
    u = Unihandecoder(lang="zh")
    assert u.decode(case) == expected


def test_kana():
    u = Unihandecoder(lang="ja")
    for n in range(0x3000, 0x30ff):
        # Just check that it doesn't throw an exception
        t = chr(n)
        u.decode(t)


@pytest.mark.xfail(reason="Chinese handling in preference to ja is not unexpected.")
@pytest.mark.parametrize("case, expected", [
    ('\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f', 'Ashita ha Ashita no Kaze ga Fuku'),
    ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439", 'Mei Tenmei Ten Teki Sui'),
    # (u"馮", "Fuu"), # Fuu in human's name, Hyou in another case
    # regression tests
    ('\u30d0\u30cb\u30fc\u3061\u3083\u3093\u3061\u306e\u30b7\u30e3\u30ef\u30fc\u30ce\u30ba\u30eb\u306e\u5148\u7aef',
     "bani- chanchino shawa-nozuru no Sentan"),  # test for u30fc
    ('\u3093\u301c\u30fb\u30fb\u30fb\u3002\u30b1\u30c4\u3063!\uff01', "n ~.... ketsu tsu !!"),
    # Hiragana n Namisen katakana-middle-dot
    # dot dot Touten, katakana KE, katakana
    # TSU, Hiragana small TU, ASCII !, half width !
    ("ページへようこそ", 'pe-ji heyoukoso'),
    ("森鴎外", 'Mori Ougai'),  # no-itaiji
    ("森鷗外", 'Mori Ougai'),   # itaiji
    ("する。", 'suru.'),  # end mark test
    ("森鷗外", 'Mori Ougai'),  # itaiji
])
def test_ja(case, expected):
    assert Unihandecoder(lang="ja").decode(case) == expected


@pytest.mark.parametrize("case, expected", [
    ('\ub0b4\uc77c\uc740 \ub0b4\uc77c \ubc14\ub78c\uc774 \ubd84\ub2e4', 'naeileun naeil barami bunda'),
    ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439", 'Myeng Chen Myeng Chen Cek Feng Chwi ')
])
def test_kr(case, expected):
    assert Unihandecoder(lang="kr").decode(case) == expected


@pytest.mark.parametrize("case, expected", [
    ("\u3400", 'Qiu '),
    ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439", 'Ming Tian Ming Tian De Feng Chui '),
    ("馮", "Feng "),
])
def test_zh(case, expected):
    assert Unihandecoder(lang="zh").decode(case) == expected


@pytest.mark.parametrize("case, expected", [
    ('Ng\xe0y mai gi\xf3 th\u1ed5i v\xe0o ng\xe0y mai', 'Ngay mai gio thoi vao ngay mai'),
    ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439", 'Minh Tian Minh Tian De Feng Xuy ')
])
def test_vn(case, expected):
    assert Unihandecoder(lang="vn").decode(case) == expected


def test_yue():
    YUETESTS = [('香港', 'Hoeng Gong ')]
    u = Unihandecoder(lang="yue")
    for case, expected in YUETESTS:
        assert u.decode(case) == expected


@pytest.mark.parametrize("source, expected", [
    ('\N{LATIN SMALL LETTER E}\N{COMBINING CIRCUMFLEX ACCENT}', 'e'),
    ('\U0000304B\U00003099', 'ga')
])
def test_composition(source, expected):
    assert Unihandecoder().decode(source) == expected
