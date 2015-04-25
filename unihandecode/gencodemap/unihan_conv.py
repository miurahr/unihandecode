#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re
import bz2

try:
    from cPickle import dump
except:
    from pickle import dump

#python 2,3 compatibility
try:
    unicode # python2
    def u(str): return str.decode("utf-8")
    pass
except: #python 3
    def u(str): return str
    pass

class UnihanConv():

    readings = {}
    firsttime = True
    lang = None
    priority = {
        'kr':  [ 'kKorean', 'kMandarin', 'kJapaneseOn', 'kVietnamese', 'kCantonese', 'kHanyuPinyin', 'kJapaneseKun'],
        'zh': [ 'kMandarin', 'kCantonese', 'kKorean',  'kJapaneseOn', 'kVietnamese', 'kHanyuPinyin', 'kJapaneseKun'],
        'ja': [ 'kJapaneseOn', 'kJapaneseKun', 'kMandarin', 'kCantonese', 'kKorean',  'kVietnamese', 'kHanyuPinyin'],
        'vn': [ 'kVietnamese', 'kMandarin', 'kCantonese', 'kJapaneseOn', 'kJapaneseKun', 'kKorean',  'kHanyuPinyin'],
    }
    pmap = {
        ord(u('â')):'a',ord(u('à')):'a',ord(u('ắ')):'a',ord(u('ă')):'a',ord(u('ấ')):'a',
        ord(u('ü')):'u',ord(u('ụ')):'u',ord(u('ú')):'u',ord(u('ử')):'u',ord(u('ư')):'u',
        ord(u('ù')):'u',
        ord(u('é')):'e',
        ord(u('ọ')):'o',ord(u('ố')):'o',ord(u('ộ')):'o',ord(u('ơ')):'o',ord(u('ớ')):'o',
        ord(u('ớ')):'o',   
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
        out_fn = dest + '.bz2'
        outfile = bz2.BZ2File(out_fn, 'w', 1024**2, 9)
        try:
            dump((tbl, max_len), outfile, protocol=2)
        finally:
            outfile.close()

    def check_category(self, lcode, category, pron):
        try:        
            p = self.priority[self.lang].index(category)
        except:
            return

        if not ((lcode in self.readings) and (self.readings[lcode][1] < p)):
            if category in ['kMandarin', 'kCantonese']:
                self.readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1 ',pron), p)
            elif category == 'kHanyuPinyin':
                self.readings[lcode] = (re.sub(r'\w+\.\w+:(\w+)',r'\1 ',pron), p)
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
                    tmap.append(reading.encode("utf-8"))
            else:
                tmap.append('')
        tbl['x%x'%ucode] = tmap

    def process_readings(self, source, tbl):
        oucode = 0

        r1 = re.compile(r'U\+([0-9A-F]{2,3})([0-9A-F]{2}\b)')
        for line in open(source, 'r'):
            try:
                uline = unicode(line, "utf-8") # python2
                items = uline[:-1].split('\t')
                pass
            except:
                items = line[:-1].split('\t') # python3
                pass
            
            try:
                code = r1.sub(r'\1\t\2',items[0]).split('\t')
                category = items[1]
                ptmp = items[2].split(' ')[0].capitalize()
                pron = re.sub('[^\00-\x7f]', lambda x: self.pmap[ord(x.group())], ptmp) 
            except:
                continue

            if code is None:
                continue

            ucode = int(code[0],16)
            lcode = int(code[1],16)
            if (oucode != ucode):
                self.gen_map(tbl, oucode)
                oucode = ucode 
                self.readings={}
            self.check_category(lcode, category, pron)

        self.gen_map(tbl, oucode) # output when eof

