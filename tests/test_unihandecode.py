# -*- coding: utf-8 -*-
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unihandecode import Unihandecoder

try:
    t = unichr(1)
except:
    def unichr(n):
        return chr(n)

class TestUnihandecode(unittest.TestCase):
    def test_ascii(self):
        u = Unihandecoder(lang="zh")
        for n in range(0,128):
            t = chr(n)
            self.assertEqual(u.decode(t), t)

    def test_bmp(self):
        u = Unihandecoder(lang="zh")
        for n in range(0,0x10000):
            # Just check that it doesn't throw an exception
            try:
                t = unichr(n)
                u.decode(t)
            except:
                print("catch error at %02x"%n)


    def test_mathematical_latin(self):
        # 13 consecutive sequences of A-Z, a-z with some codepoints
        # undefined. We just count the undefined ones and don't check
        # positions.
        if sys.maxunicode < 0x1d6a4:
            print("skip test because of Narrow Python")
            return

        empty = 0
        u = Unihandecoder(lang="zh")
        for n in range(0x1d400, 0x1d6a4):
            if n % 52 < 26:
                a = chr(ord('A') + n % 26)
            else:
                a = chr(ord('a') + n % 26)
            b = u.decode(unichr(n))

            if not b:
                empty += 1
            else:
                self.assertEqual(b, a)

        self.assertEqual(empty, 24)

    def test_mathematical_digits(self):
        if sys.maxunicode < 0x1d800:
            print("skip test because of Narrow Python")
            return

        u = Unihandecoder(lang="zh")
        # 5 consecutive sequences of 0-9
        for n in range(0x1d7ce, 0x1d800):
            a = chr(ord('0') + (n-0x1d7ce) % 10)
            b = u.decode(unichr(n))

            self.assertEqual(b, a)

    def test_combining_chars(self):
        TESTS = [
                #  roman number "1"  wrapped with solid square 
                (u"\u0031\u20de",    "1"), 
                ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_decomposed_form(self):
        TESTS = [
                (u"\u0041\u0301", "A"),  # "A" with accent mark 
                (u"\u0061\u0323\u0302", "a"), #  "a" with accent marks
                (u"\u30AB\u3099", "ga"), # "ガ" coded by decomposed from as ' カ゛ '
                (u"\u304B\u3099", "ga"), # "が" coded by decomposed from as ' か゛ '
                ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_squared_chars(self):
        TESTS = [
                (u"\u3301", "alpha"), # combined Alpha in Katakana
                (u"\u3302", "ampere"), # combined Ampere in Katakana 
                (u"\u3304", "inning"),
                (u"\u3306", "won"), # combined Won in Katakana
                (u"\u3307", "escudo"), 
                (u"\u3308", "acre"), # combined Acre in Katakana
                (u"\u3309", "ounce"), # combined ounce in Katakana
                (u"\u330a", "ohm"), # combined Ohm in Katakana
                (u"\u3349", "milli"), # milli in Katakana
                (u"\u3314", "kilo"), # kilo in Katakana
                (u"\u3315", "kilogram"), # kilo gram in Katakana
                (u"\u3316", "kilometer"), # kilo metre in Katakana
                (u"\u3322", "centi"), # centi in Katakana
                (u"\u334d", "meter"), #metre in Katakana
                (u"\u3318", "gram"), # gram in Katakana
                (u"\u3327", "ton"), # ton in Katakana
                (u"\u3303", "are"), # are in Katakana
                (u"\u3336", "hectare"), # hect-are in Katakana
                (u"\u337f", "Inc."), # kabusiki kaisha in Katakana
               ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_compatibility_composite(self):
        TESTS = [
                (u"\ufb01","fi"),
                (u"\u0032\u2075", "25"),
                       ]
        u = Unihandecoder(lang="zh")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_mac_japanese_pua(self):
        TESTS = [
                (u"\uF862\u6709\u9650\u4F1A\u793E",  #Adobe CID 8321
                "Yuugengaisha"),
                (u"\u5927\u20dd", "Dai "),  # "大" with circle
                (u"\u5c0f\u20dd", "Shou "), # "小" with circle
                (u"\u63a7\u20dd", "Hikae "),  # "控" with circle
                    ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_specific_bmp(self):

        TESTS = [
                (u"Hello, World!", 
                "Hello, World!"),

                (u"'\"\r\n",
                 "'\"\r\n"),

                (u"ČŽŠčžš",
                 "CZSczs"),

                (u"\u00a0\u00a1\u00a2\u00a3\u00a4\u00a5\u00a6\u00a7",
                  u" !C/PS\u005c$?Y=|SS"),
                (u"\u00a8\u00a9\u00aa\u00ab\u00ac\u00ad\u00ae\u00af",
                  u"\u0022(c)a<<!(r)-"),

                (u"ア",
                 "a"),

                (u"α",
                "a"),

                (u"а",
                "a"),

                (u'ch\xe2teau',
                "chateau"),

                (u'vi\xf1edos',
                "vinedos"),
                
                (u"\u5317\u4EB0",
                "Bei Jing "),

                (u"Efﬁcient",
                "Efficient"),

                # Table that doesn't exist
                (u'\ua500',
                ''),
                
                # Table that has less than 256 entriees
                (u'\u1eff',
                ''),

                # Mark area
                (u"\u210a",  #gram mark
                "g"),

            ]

        u = Unihandecoder(lang="zh")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_specific_supplementary(self):
        if sys.maxunicode < 0x1d6a4:
            print("skip test because of Narrow Python")
            return

        TESTS = [
                # Non-BMP character
                (u'\U0001d5a0',
                'A'),

                # Mathematical
                (u'\U0001d5c4\U0001d5c6/\U0001d5c1',
                'km/h'),
        ]
        u = Unihandecoder(lang="zh")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_kana(self):
        u = Unihandecoder(lang="ja")
        for n in range(0x3000,0x30ff):
            # Just check that it doesn't throw an exception
            try:
                t = unichr(n)
                u.decode(t)
            except:
                print("catch error at %02x"%n)

    def test_ja(self):
        JATESTS = [
            (u'\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f',
            'Ashita ha Ashita no Kaze ga Fuku'),
            (u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
            'Mei Tenmei Ten Teki Sui'),
            # (u"馮", "Fuu"), # Fuu in human's name, Hyou in another case
            # regression tests
            (u'\u30d0\u30cb\u30fc\u3061\u3083\u3093\u3061\u306e\u30b7\u30e3\u30ef\u30fc\u30ce\u30ba\u30eb\u306e\u5148\u7aef',
            "bani- chanchino shawa-nozuru no Sentan"),   # test for u30fc
            (u'\u3093\u301c\u30fb\u30fb\u30fb\u3002\u30b1\u30c4\u3063!\uff01',
            "n ~.... ketsu tsu !!"), #Hiragana n Namisen katakana-middle-dot
                                     #dot dot Touten, katakana KE, katakana
                                     #TSU, Hiragana small TU, ASCII !, half width !
            (u"ページへようこそ", 'pe-ji heyoukoso'),
            (u"森鴎外",'Mori Ougai'), # no-itaiji
            (u"森鷗外",'Mori Ougai'), # itaiji
            (u"する。",'suru.'),# end mark test
            ]
        u = Unihandecoder(lang="ja")
        for input, output in JATESTS:
            self.assertEqual(u.decode(input), output)

    def test_ja_itaiji(self):
        JATESTS = [
            (u"森鷗外",'Mori Ougai'), # itaiji
           ]
        u = Unihandecoder(lang="ja")
        for input, output in JATESTS:
            self.assertEqual(u.decode(input), output)

    def test_kr(self):
        KRTESTS = [
            (u'\ub0b4\uc77c\uc740 \ub0b4\uc77c \ubc14\ub78c\uc774 \ubd84\ub2e4',
                'naeileun naeil barami bunda'),
            (u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
             'Myeng Chen Myeng Chen Cek Feng Chwi ')
            ]
        u = Unihandecoder(lang="kr")
        for input, output in KRTESTS:
            self.assertEqual(u.decode(input), output)

    def test_zh(self):
        ZHTESTS = [
            (u"\u3400", 'Qiu '),
            (u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
             'Ming Tian Ming Tian De Feng Chui '),
            (u"馮", "Feng "),
            ]
        u = Unihandecoder(lang="zh")
        for input, output in ZHTESTS:
            self.assertEqual(u.decode(input), output)

    def test_vn(self):
        VNTESTS = [
            (u'Ng\xe0y mai gi\xf3 th\u1ed5i v\xe0o ng\xe0y mai',
            'Ngay mai gio thoi vao ngay mai'),
            (u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
            'Minh Tian Minh Tian De Feng Xuy ')
            ]
        u = Unihandecoder(lang="vn")
        for input, output in VNTESTS:
            self.assertEqual(u.decode(input), output)

    def test_yue(self):
        YUETESTS = [
            (u'香港',
            'Hoeng Gong '),
            ]
        u = Unihandecoder(lang="yue")
        for input, output in YUETESTS:
            self.assertEqual(u.decode(input), output)

if __name__ == "__main__":
    unittest.main()
