#!/usr/bin/env python
import sys
import re
import getopt

source = 'Unihan_Readings.txt'
olcode  = 0
firsttime = True
readings={}

def main(argv):
    print_header()
    process_readings()
    print_footer()


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
            print "'"+readings[i]+"',",
        else:
            print  "'',",
        if (i % 16) == 15:
            print "\n"+" "*12,  

def parse_line(lcode, category, pron):
    global readings
    if category == 'kKorea':
        readings[lcode] = pron
    elif category == 'kMandarin' and (not readings.has_key(lcode)):
        readings[lcode] = re.sub(r'(\w+)[1-5]',r'\1',pron)


def process_readings():
    global readings
    oucode = 0
    for line in open(source,'r'):
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
    main(sys.argv[1:])

