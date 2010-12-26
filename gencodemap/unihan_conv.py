#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re

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
        fout = open(dest,'w')
        fout.write("# -*- coding: utf-8 -*-\n\n__license__ = \'GPL 3\'\n\
__copyright__ = \'2010 Hiroshi Miura <miurahr@linux.com>\'\n__docformat__ = \'restructuredtext en\'\n\
\n\'\'\'\nUnicode code point dictionary.\nBased on Unicode.org Unihan database.\n\'\'\'\n\n")
        self.process_readings(source, fout)
        fout.write("]\n}\n")
        fout.close()

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

    def gen_map(self,fout, ucode):
        if ucode is 0:
            return

        if self.firsttime:
            self.firsttime = False
            fout.write("CODEPOINTS = { \n    'x%x':[\n        "%ucode)
        else:
            fout.write("],\n    'x%x':[\n        "%ucode)

        for i in range(0, 256):
            if i in self.readings:
                reading = self.readings[i][0]
                if all(ord(c) < 128 for c in reading):
                    fout.write("'"+reading+"',")
                else:
                    fout.write("'"+reading.encode("utf-8")+"', #XXX\n        ")
                    # if ??codepoints.py file has XXX, you need fix pmap[x] 
            else:
                fout.write("'',")
            if (i % 16) == 15:
                fout.write("\n"+" "*8)

    def process_readings(self, source, fout):
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
                self.gen_map(fout, oucode)
                oucode = ucode 
                self.readings={}
            self.check_category(lcode, category, pron)
    
        self.gen_map(fout, oucode) # output when eof

