#!/usr/bin/env python
import sys
import re
import getopt
from unidecode import unidecode
import codecs


def unihan_conv(source='Unihan_Readings.txt', dest='../unihandecode/krcodepoints.py', lang='kr'):
    global parse_line

    if lang == 'kr':
        parse_line = k_parse_line
    elif lang == 'ja':
        parse_line = j_parse_line
    elif lang == 'vn':
        parse_line = v_parse_line
    else:
        parse_line = c_parse_line

    saveout = sys.stdout
    fout = open(dest,'w')
    sys.stdout = fout

    print_header()
    process_readings(source)
    print_footer()


    sys.stdout = saveout
    fout.close()


def c_parse_line(lcode, category, pron):
    # priority is 
    # Korean     = 1
    # Mandarin   = 2
    # JapaneseOn = 3
    # Vietnamese = 4
    global readings
    if category == 'kMandarin':
        readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1',pron), 1)
    elif category == 'kKorean' and not (readings.has_key(lcode) and readings[lcode][1] > 2):
        readings[lcode] = (pron, 2)
    elif category == 'kJapaneseOn' and not (readings.has_key(lcode) and readings[lcode][1] > 3):
        readings[lcode] = (pron, 3)
    elif category == 'kVietnamese' and not (readings.has_key(lcode) and readings[lcode][1] > 4):
        readings[lcode] = (unidecode(unicode(pron,"utf-8")), 4)

def k_parse_line(lcode, category, pron):
    # priority is 
    # Korean     = 1
    # Mandarin   = 2
    # JapaneseOn = 3
    # Vietnamese = 4
    global readings
    if category == 'kKorean':
        readings[lcode] = (pron, 1)
    elif category == 'kMandarin' and not (readings.has_key(lcode) and readings[lcode][1] > 2):
        readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1',pron), 2)
    elif category == 'kJapaneseOn' and not (readings.has_key(lcode) and readings[lcode][1] > 3):
        readings[lcode] = (pron, 3)
    elif category == 'kVietnamese' and not (readings.has_key(lcode) and readings[lcode][1] > 4):
        readings[lcode] = (unidecode(unicode(pron,"utf-8")), 4)

def j_parse_line(lcode, category, pron):
    # priority is 
    # Korean     = 4
    # Mandarin   = 3
    # JapaneseOn = 1
    # JapaneseKun = 2
    # Vietnamese = 5
    global readings
    if category == 'kJapaneseOn':
        readings[lcode] = (pron, 1)
    if category == 'kJapaneseKun' and not (readings.has_key(lcode) and readings[lcode][1] > 2):
        readings[lcode] = (pron, 2)
    elif category == 'kMandarin' and not (readings.has_key(lcode) and readings[lcode][1] > 3):
        readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1',pron), 3)
    elif category == 'kKorean' and not (readings.has_key(lcode) and readings[lcode][1] > 4):
        readings[lcode] = (pron, 4)
    elif category == 'kVietnamese' and not (readings.has_key(lcode) and readings[lcode][1] > 5):
        readings[lcode] = (unidecode(unicode(pron,"utf-8")), 5)

def v_parse_line(lcode, category, pron):
    # priority is 
    # Korean     = 4
    # Mandarin   = 2
    # JapaneseOn = 3
    # Vietnamese = 1
    global readings
    if category == 'kVietnamese':
        readings[lcode] = (unidecode(unicode(pron,"utf-8")), 1)
    elif category == 'kMandarin' and not (readings.has_key(lcode) and readings[lcode][1] > 2):
        readings[lcode] = (re.sub(r'(\w+)[1-5]',r'\1',pron), 2)
    elif category == 'kJapaneseOn' and not (readings.has_key(lcode) and readings[lcode][1] > 3):
        readings[lcode] = (pron, 3)
    elif category == 'kKorean' and not (readings.has_key(lcode) and readings[lcode][1] > 4):
        readings[lcode] = (pron, 4)


def print_header():
    print "\
# -*- coding: utf-8 -*-\n\
\n\
__license__ = \'GPL 3\'\n\
__copyright__ = \'2010 Hiroshi Miura <miurahr@linux.com>\'\n\
__docformat__ = \'restructuredtext en\'\n\
\n\
\'\'\'\n\
Unicode code point dictionary.\n\
Based on Unicode.org Unihan database.\n\
\'\'\'\n\
\n\
"
def print_footer():
    print "]\n}\n"   


def gen_map(ucode):
    global firsttime, readings
    if ucode ==0:
        return

    if firsttime:
        firsttime = False
        print "CODEPOINTS = { \n      u'x%x':["%ucode,
    else:
        print "\n      ],\n      u'x%x':["%ucode,

    for i in range(0, 255):
        if readings.has_key(i):
            print "'"+readings[i][0]+"',",
        else:
            print  "'',",
        if (i % 16) == 15:
            print "\n"+" "*12,  

def process_readings(source):
    global readings,firsttime, parse_line

    oucode = 0
    firsttime = True
    readings = {}

    for line in open(source, 'r'):
        items = line[:-1].split('\t')
        try:
            code = re.sub(r'U\+([0-9A-F]{2})([0-9A-F]{2}\b)',r'\1\t\2',items[0]).split('\t')
            category = items[1]
            pron = items[2].split(' ')[0].capitalize()

            if code is not None:
                ucode = int(code[0],16)
                lcode = int(code[1],16)
                if (oucode != ucode):
                    gen_map(oucode) 
                    oucode = ucode 
                    readings={}
                parse_line(lcode, category, pron)

        except:
            continue
    gen_map(oucode) # output when eof


if __name__ == "__main__":
    unihan_kconv()

