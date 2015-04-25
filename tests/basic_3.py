# -*- coding: utf-8 -*-
import unittest
from unihandecode import Unihandecoder

class TestUnidecode(unittest.TestCase):
    def test_ascii(self):
        u = Unihandecoder()
        for n in range(0,128):
            t = chr(n)
            self.assertEqual(u.decode(t), t)

    def test_combining_chars(self):
        TESTS = [
                ("\u0031\u20de",    "1"),
                    ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_decomposed_form(self):
        TESTS = [
                ("\u0041\u0301", "A"),
                ("\u0061\u0323\u0302", "a"),
                ("\u304B\u3099", "ga"),
                ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_mac_japanese_pua(self):
        TESTS = [
                ("\uF862\u6709\u9650\u4F1A\u793E",
                "Yuugengaisha"),
                    ]
        u = Unihandecoder(lang="ja")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_bmp(self):
        u = Unihandecoder()
        for n in range(0,0x10000):
            # Just check that it doesn't throw an exception
            t = chr(n)
            u.decode(t)
            
    def test_mathematical_latin(self):
        # 13 consecutive sequences of A-Z, a-z with some codepoints
        # undefined. We just count the undefined ones and don't check
        # positions.
        empty = 0
        u = Unihandecoder()
        for n in range(0x1d400, 0x1d6a4):
            if n % 52 < 26:
                a = chr(ord('A') + n % 26)
            else:
                a = chr(ord('a') + n % 26)
            b = u.decode(chr(n))
            
            if not b:
                empty += 1
            else:
                self.assertEqual(b, a)
                
        self.assertEqual(empty, 24)
                
    def test_mathematical_digits(self):
        # 5 consecutive sequences of 0-9
        u = Unihandecoder()
        for n in range(0x1d7ce, 0x1d800):
            a = chr(ord('0') + (n-0x1d7ce) % 10)
            b = u.decode(chr(n))
            
            self.assertEqual(b, a)

    def test_specific_bmp(self):

        TESTS = [
                ("Hello, World!", 
                "Hello, World!"),

                ("'\"\r\n",
                 "'\"\r\n"),

                ("ČŽŠčžš",
                 "CZSczs"),

                ("ア",
                 "a"),

                ("α",
                "a"),

                ("а",
                "a"),

                ('ch\xe2teau',
                "chateau"),

                ('vi\xf1edos',
                "vinedos"),
                
                ("\u5317\u4EB0",
                "Bei Jing "),

                ("Efﬁcient",
                "Efficient"),

                # Table that doesn't exist
                ('\ua500',
                ''),
                
                # Table that has less than 256 entriees
                ('\u1eff',
                ''),
  
                # Mark area
                ("\u210a",  #gram mark
                "g"),
          ]
        u = Unihandecoder()
        for instr, output in TESTS:
            self.assertEqual(u.decode(instr), output)

    def test_specific_ext(self):

        TESTS = [
                # Non-BMP character
                ('\U0001d5a0',
                'A'),

                # Mathematical
                ('\U0001d5c4\U0001d5c6/\U0001d5c1',
                'km/h'),
        ]
        u = Unihandecoder(lang="zh")
        for input, output in TESTS:
            self.assertEqual(u.decode(input), output)

    def test_ja(self):
        JATESTS = [
            ('\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f',
            'Ashita ha Ashita no Kaze ga Fuku'),
            ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
            'Mei Tenmei Ten Teki Sui'),
            ("馮", "Fuu"), # Fuu in human's name, Hyou in another case
            # regression tests
            ('\u30d0\u30cb\u30fc\u3061\u3083\u3093\u3061\u306e\u30b7\u30e3\u30ef\u30fc\u30ce\u30ba\u30eb\u306e\u5148\u7aef',
            "bani-chanchinoshawa-nozuruno Sentan"),  # test for u30fc
            ('\u3093\u301c\u30fb\u30fb\u30fb\u3002\u30b1\u30c4\u3063!\uff01',
            "n ~ .... ketsutsu !!"), #Hiragana n Namisen katakana-middle-dot
                                     #dot dot Touten, katakana KE, katakana
                                     #TSU, Hiragana small TU, ASCII !, half width !
            ("ページへようこそ", 'pe-jiheyoukoso'),
            ("する。",'suru. '), # end mark test
            ]
        u = Unihandecoder(lang="ja")
        for instr, output in JATESTS:
            self.assertEqual(u.decode(instr), output)

    def test_kr(self):
        KRTESTS = [
            ('\ub0b4\uc77c\uc740 \ub0b4\uc77c \ubc14\ub78c\uc774 \ubd84\ub2e4',
                'naeileun naeil barami bunda'),
            ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
             'Myeng Chen Myeng Chen Cek Feng Chwi ')
            ]
        u = Unihandecoder(lang="kr")
        for instr, output in KRTESTS:
            self.assertEqual(u.decode(instr), output)

    def test_zh(self):
        ZHTESTS = [
            ('\u660e\u5929\u660e\u5929\u7684\u98ce\u5439',
             'Ming Tian Ming Tian De Feng Chui ')
            ]
        u = Unihandecoder(lang="zh")
        for instr, output in ZHTESTS:
            self.assertEqual(u.decode(instr), output)

    def test_vn(self):
        VNTESTS = [
            ('Ng\xe0y mai gi\xf3 th\u1ed5i v\xe0o ng\xe0y mai',
            'Ngay mai gio thoi vao ngay mai'),
            ("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439",
            'Minh Tian Minh Tian De Feng Xuy ')
            ]
        u = Unihandecoder(lang="vn")
        for input, output in VNTESTS:
            self.assertEqual(u.decode(input), output)

