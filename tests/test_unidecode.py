# -*- coding: utf-8 -*-
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unihandecode import unidecode

try:
    t = unichr(1)
except:
    def unichr(n):
        return chr(n)

class TestUnidecode(unittest.TestCase):
    def test_unidecode_ascii(self):
        for n in range(0,128):
            t = chr(n)
            self.assertEqual(unidecode(t), t)

    def test_unidecode_bmp(self):
        for n in range(0,0x10000):
            # Just check that it doesn't throw an exception
            try:
                t = unichr(n)
                unidecode(t)
            except:
                print("catch error at %02x"%n)


    def test_unidecode_mathematical_latin(self):
        # 13 consecutive sequences of A-Z, a-z with some codepoints
        # undefined. We just count the undefined ones and don't check
        # positions.
        if sys.maxunicode < 0x1d6a4:
            print("skip test because of Narrow Python")
            return

        empty = 0
        for n in range(0x1d400, 0x1d6a4):
            if n % 52 < 26:
                a = chr(ord('A') + n % 26)
            else:
                a = chr(ord('a') + n % 26)
            b = unidecode(unichr(n))

            if not b:
                empty += 1
            else:
                self.assertEqual(b, a)

        self.assertEqual(empty, 24)

    def test_unidecode_mathematical_digits(self):
        if sys.maxunicode < 0x1d800:
            print("skip test because of Narrow Python")
            return

        # 5 consecutive sequences of 0-9
        for n in range(0x1d7ce, 0x1d800):
            a = chr(ord('0') + (n-0x1d7ce) % 10)
            b = unidecode(unichr(n))

            self.assertEqual(b, a)

    def test_unidecode_combining_chars(self):
        TESTS = [
                #  roman number "1"  wrapped with solid square 
                (u"\u0031\u20de",    "1"), 
                ]
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_decomposed_form(self):
        TESTS = [
                (u"\u0041\u0301", "A"),  # "A" with accent mark 
                (u"\u0061\u0323\u0302", "a"), #  "a" with accent marks
                (u"\u30AB\u3099", "ga"), # "ガ" coded by decomposed from as ' カ゛ '
                (u"\u304B\u3099", "ga"), # "が" coded by decomposed from as ' か゛ '
                ]
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_squared_chars(self):
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
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_compatibility_composite(self):
        TESTS = [
                (u"\ufb01","fi"),
                (u"\u0032\u2075", "25"),
                       ]
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_mac_japanese_pua(self):
        TESTS = [
                (u"\uF862\u6709\u9650\u4F1A\u793E",  #Adobe CID 8321
                "You Xian Hui She "), # "yuugengaisha" in unihandecode(ja)
                (u"\u5927\u20dd", "Da "),  # "大" with circle "Dai " in unihandecode(ja)
                (u"\u5c0f\u20dd", "Xiao "), # "小" with circle "Shou " in unihandecode(ja)
                (u"\u63a7\u20dd", "Kong "),  # "控" with circle "Hikae " in unihandecode(ja)
                    ]
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_specific_bmp(self):

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
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_specific_supplementary(self):
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
        for input, output in TESTS:
            self.assertEqual(unidecode(input), output)

    def test_unidecode_kana(self):
        for n in range(0x3000,0x30ff):
            # Just check that it doesn't throw an exception
            try:
                t = unichr(n)
                unidecode(t)
            except:
                print("catch error at %02x"%n)

    def test_unidecode_zh(self):
        ZHTESTS = [
            (u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
             'Ming Tian Ming Tian De Feng Chui '),
            (u"馮", "Feng "),
            ]
        for input, output in ZHTESTS:
            self.assertEqual(unidecode(input), output)

if __name__ == "__main__":
    unittest.main()
