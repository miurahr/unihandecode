#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pickle
from typing import Dict

__license__ = 'GPL 3'
__copyright__ = '2010,2018, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'


class UnihanConv():

    readings = {}  # type: Dict[str, str]
    firsttime = True
    lang = None
    priority = {
        'kr':  [ 'kKorean', 'kMandarin', 'kJapaneseOn', 'kVietnamese', 'kCantonese', 'kJapaneseKun'],
        'zh': [ 'kMandarin', 'kCantonese', 'kKorean',  'kJapaneseOn', 'kVietnamese', 'kJapaneseKun'],
        'yue': [ 'kCantonese', 'kMandarin', 'kKorean',  'kJapaneseOn', 'kVietnamese', 'kJapaneseKun'],
        'ja': [ 'kJapaneseOn', 'kJapaneseKun', 'kMandarin', 'kCantonese', 'kKorean',  'kVietnamese'],
        'vn': [ 'kVietnamese', 'kMandarin', 'kCantonese', 'kJapaneseOn', 'kJapaneseKun', 'kKorean'],
    }
    pronounce_char_map = {
        'â':'a','à':'a','ắ':'a','ă':'a','ấ':'a',
        'ü':'u','ụ':'u','ú':'u','ử':'u','ư':'u',
        'ù':'u',
        'é':'e',
        'ọ':'o','ố':'o','ộ':'o','ơ':'o','ớ':'o',
     }

    def __init__(self, lang):
        if lang in self.priority:
            self.lang = lang
        else:
            self.lang = 'zh'

    def run(self, source, dest):
        max_len = 0
        tbl = {}
        self.process_readings(source, tbl)
        max_len = max(max_len, len(tbl))
        with open(dest, 'wb') as outfile:
            pickle.dump((tbl, max_len), outfile)

    def check_category(self, lcode, category, pron):
        try:        
            p = self.priority[self.lang].index(category)
        except:
            return

        if not ((lcode in self.readings) and (self.readings[lcode][1] < p)):
            if category in ['kMandarin', 'kCantonese']:
                self.readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1 ',pron), p)
            elif category == 'kHanyuPinyin': # pragma: no branch
                self.readings[lcode] = (re.sub(r'\w+\.\w+:(\w+)',r'\1 ',pron), p) # pragma: no cover
            else:
                self.readings[lcode] = ("%s "%pron, p)

    def gen_map(self, tbl, ucode):
        if ucode is 0:
            return

        tmap = []
        for i in range(0, 256):
            if i in self.readings:
                reading = self.readings[i][0]
                if all(ord(c) < 128 for c in reading):
                    tmap.append(reading)
                else:
                    tmap.append(reading.encode("utf-8")) # pragma: no cover
            else:
                tmap.append('')
        tbl['x%x'%ucode] = tmap

    def process_readings(self, source, tbl): # pragma: no cover
        with open(source, 'r', encoding='utf8') as f:
            self.process_file(f, tbl)

    def process_file(self, f, tbl):
        oucode = 0

        # Retrive U+XXXX from a first of line in a definition
        # for example;
        # U+3432	kMandarin	DAI4
        # r1 is a expression to separate upper byte and lower byte.
        r1 = re.compile(r'U\+([0-9A-F]{2,3})([0-9A-F]{2}\b)')
        for line in f:
            items = line[:-1].split('\t')
            
            try:
                # code[0] is upper byte and code[1] is lower byte
                # for example; U+3432 become code[0]='34', code[1]='32'
                # then ucode=0x34, lcode=0x32
                code = r1.sub(r'\1\t\2',items[0]).split('\t')
                category = items[1]
                # Remove Diacritical mark from pronounciation description
                # to generate transiliteration words and then capitalize
                pron = re.sub('[^\00-\x7f]',
                              lambda x: self.pronounce_char_map[x.group()],
                                        items[2].split(' ')[0]).capitalize()
            except:
                continue

            if code is None:
                continue # pragma: no cover

            ucode = int(code[0],16)
            lcode = int(code[1],16)

            # produce map for each upper byte ucode
            if (oucode != ucode):
                self.gen_map(tbl, oucode)
                oucode = ucode 
                self.readings={}
            self.check_category(lcode, category, pron)

        self.gen_map(tbl, oucode) # output when eof

