#!/usr/bin/env python
import sys
import re

def print_header():
    print "\
__license__ = \'GPL 3\'\n\
__copyright__ = \'2010 Hiroshi Miura <miurahr@linux.com>\'\n\
__docformat__ = \'restructuredtext en\'\n\
\n\
\'\'\'\n\
Unicode HAN code point dictionary.\n\
Based on Unicode.org Unihan database.\n\
\'\'\'\n\
\n\
CODEPOINTS = {\n\
"

def process_readings():
    oucode = 0
    olcode  = 0
    for line in open('Unihan_Readings.txt','r'):
        items = line[:-1].split('\t')
        try:
            r = re.match(r'kKorea', items[1])
            if r is not None:
                code = re.sub(r'U\+([0-9A-F]{2})([0-9A-F]{2})',r'\1\t\2',items[0]).split('\t')
                ucode = int(code[0],16)
                lcode = int(code[1],16)
                pron = items[2].split(' ')[0].capitalize()

                if oucode != ucode:
                    print "],\nu'x%s':["%code[0],
                    oucode = ucode
                    olcode = -1
                if (lcode - olcode) > 1:
                    for i in range(lcode-olcode-1):
                        print  '"[?]",',
                olcode = lcode
                print  '"'+pron+'",',
        except:
            continue

def print_footer():
    print "}"

print_header()
process_readings()
print_footer()
