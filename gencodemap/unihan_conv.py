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

    parse_line = None
    readings = {}
    firsttime = True

    def __init__(self, lang):
        if lang is 'kr':
            self.parse_line = self.k_parse_line
        elif lang is 'ja':
            self.parse_line = self.j_parse_line
        elif lang is 'vn':
            self.parse_line = self.v_parse_line
        else:
            self.parse_line = self.c_parse_line

    def run(self, source, dest):
        fout = open(dest,'w')
        fout.write("# -*- coding: utf-8 -*-\n\n__license__ = \'GPL 3\'\n\
__copyright__ = \'2010 Hiroshi Miura <miurahr@linux.com>\'\n__docformat__ = \'restructuredtext en\'\n\
\n\'\'\'\nUnicode code point dictionary.\nBased on Unicode.org Unihan database.\n\'\'\'\n\n")
        self.process_readings(source, fout)
        fout.write("]\n}\n")
        fout.close()

    def check_r(self, lcode, n):
        if lcode in self.readings:
            if self.readings[lcode][1] > n:
                return True # low priority reading
            else:
                return False # high priority reading
        else:
            return True # still don't exist 


    def c_parse_line(self, lcode, category, pron):
        # priority is 
        # Korean     = 1
        # Mandarin   = 2
        # JapaneseOn = 3
        # Vietnamese = 4
        if category == 'kMandarin':
            self.readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1 ',pron), 1)
        elif category == 'kKorean'     and self.check_r(lcode, 2):
            self.readings[lcode] = (pron, 2)
        elif category == 'kJapaneseOn' and self.check_r(lcode, 3):
            self.readings[lcode] = ("%s "%pron, 3)
        elif category == 'kVietnamese' and self.check_r(lcode, 4):
            self.readings[lcode] = (pron, 4)
        elif category == 'kCantonese' and self.check_r(lcode, 5):
            self.readings[lcode] = (pron,5)
        elif category == 'kHanyuPinyin' and self.check_r(lcode, 6):
            self.readings[lcode] = (re.sub(r'\w+\.\w+:(\w+)',r'\1 ',pron), 6)

    def k_parse_line(self, lcode, category, pron):
        # priority is 
        # Korean     = 1
        # Mandarin   = 2
        # JapaneseOn = 3
        # Vietnamese = 4
        if category == 'kKorean':
            self.readings[lcode] = (pron, 1)
        elif category == 'kMandarin'   and self.check_r(lcode, 2):
            self.readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1 ',pron), 2)
        elif category == 'kJapaneseOn' and self.check_r(lcode, 3):
            self.readings[lcode] = ("%s "%pron, 3)
        elif category == 'kVietnamese' and self.check_r(lcode, 4):
            self.readings[lcode] = (pron, 4)
        elif category == 'kCantonese' and self.check_r(lcode, 5):
            self.readings[lcode] = (pron,5)

    def j_parse_line(self, lcode, category, pron):
        # priority is 
        # Korean     = 4
        # Mandarin   = 3
        # JapaneseOn = 1
        # JapaneseKun = 2
        # Vietnamese = 5
        if category == 'kJapaneseOn':
            self.readings[lcode] = ("%s "%pron, 1)
        elif category == 'kJapaneseKun' and self.check_r(lcode, 2):
            self.readings[lcode] = ("%s "%pron, 2)
        elif category == 'kMandarin'  and self.check_r(lcode, 3):
            self.readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1 ',pron), 3)
        elif category == 'kKorean'    and self.check_r(lcode, 4):
            self.readings[lcode] = (pron, 4)
        elif category == 'kVietnamese' and self.check_r(lcode, 5):
            self.readings[lcode] = (pron, 5)
        elif category == 'kCantonese' and self.check_r(lcode, 6):
            self.readings[lcode] = (pron,6)

    def v_parse_line(self, lcode, category, pron):
        # priority is 
        # Korean     = 4
        # Mandarin   = 2
        # JapaneseOn = 3
        # Vietnamese = 1
        if category == 'kVietnamese':
            self.readings[lcode] = (pron, 1)
        elif category == 'kMandarin'   and self.check_r(lcode, 2):
            self.readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1 ',pron), 2)
        elif category == 'kJapaneseOn' and self.check_r(lcode, 3):
            self.readings[lcode] = ("%s "%pron, 3)
        elif category == 'kKorean'     and self.check_r(lcode, 4):
            self.readings[lcode] = (pron, 4)
        elif category == 'kCantonese' and self.check_r(lcode, 5):
            self.readings[lcode] = (pron,5)


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
        pmap = {
            ord(u('â')):'a',ord(u('à')):'a',ord(u('ắ')):'a',ord(u('ă')):'a',ord(u('ấ')):'a',

            ord(u('ü')):'u',ord(u('ụ')):'u',ord(u('ú')):'u',ord(u('ử')):'u',ord(u('ư')):'u',
            ord(u('ù')):'u',

            ord(u('é')):'e',

            ord(u('ọ')):'o',ord(u('ố')):'o',ord(u('ộ')):'o',ord(u('ơ')):'o',ord(u('ớ')):'o',
            ord(u('ớ')):'o',   
         }

        r1 = re.compile(r'U\+([0-9A-F]{2,3})([0-9A-F]{2}\b)')
        for line in open(source, 'r'):
            try:
                uline = unicode(line, "utf-8")
                items = uline[:-1].split('\t')
                pass
            except:
                items = line[:-1].split('\t')
                pass
            
            try:
                code = r1.sub(r'\1\t\2',items[0]).split('\t')
                category = items[1]
                ptmp = items[2].split(' ')[0].capitalize()
                pron = re.sub('[^\00-\x7f]', lambda x: pmap[ord(x.group())], ptmp) 

                if code is not None:
                    ucode = int(code[0],16)
                    lcode = int(code[1],16)
                    if (oucode != ucode):
                        self.gen_map(fout, oucode)
                        oucode = ucode 
                        self.readings={}
                    self.parse_line(lcode, category, pron)
    
            except:
                continue
        self.gen_map(fout, oucode) # output when eof


