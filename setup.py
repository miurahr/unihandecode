#!/usr/bin/python
# derivered from unidecode setup.py

from setuptools import Command, setup, find_packages
from distutils.command.build import build

import unittest
import os,threading
import sys
import unihandecode.gencodemap as gencodemap
import unihandecode.genkanwadict as genkanwadict


def gen_map(lang):
    unihan_source = os.path.join('unihandecode','data','Unihan_Readings.txt')
    dest = os.path.join('unihandecode',lang+'codepoints.pickle')
    u = gencodemap.UnihanConv(lang)
    u.run(source = unihan_source, dest=dest)

def gen_dict(src_f, pkl_f):
    kanwa = genkanwadict.mkkanwa()
    src = os.path.join('unihandecode','data',src_f)
    dst = os.path.join('unihandecode','pykakasi',pkl_f)
    try:
        os.unlink(dst)
    except:
        pass
    kanwa.mkdict(src, dst)

def _pre_build():
    DICTS = [
        ('itaijidict.utf8', 'itaijidict2.pickle'),
        ('kanadict.utf8', 'kanadict2.pickle'),
    ]

    for (s,p) in DICTS:
        gen_dict(s, p)

    src = os.path.join('unihandecode','data','kakasidict.utf8')
    dst = os.path.join('unihandecode','pykakasi','kanwadict2') # don't add .db ext
    try:
        os.unlink(dst+'.db')
    except:
        pass
    kanwa = genkanwadict.mkkanwa()
    kanwa.run(src, dst)

    u = gencodemap.Unicodepoints()
    u.run(os.path.join('unihandecode','unicodepoints.pickle'))
    for l in ['kr','ja','zh','vn']:
        gen_map(l)

class my_build(build):
    def run(self):
        self.execute(_pre_build, (),
                    msg="Running pre build task")
        build.run(self)

setup(name='Unihandecode',
      version='0.46',
      description='US-ASCII transliterations of Unicode text',
      url='https://github.com/miurahr/unihandecode/',
      license='GPLv3/Perl',
      long_description="""
It often happens that you have non-Roman text data in Unicode, but
you can't display it -- usually because you're trying to show it
to a user via an application that doesn't support Unicode, or
because the fonts you need aren't accessible. You could represent
the Unicode characters as "???????" or "\15BA\15A0\1610...", but
that's nearly useless to the user who actually wants to read what
the text says.

What Unihandecode provides is a function, 'decode(...)' that
takes Unihancode data and tries to represent it in ASCII characters 
(i.e., the universally displayable characters between 0x00 and 0x7F). 
The representation is almost always an attempt at transliteration 
-- i.e., conveying, in Roman letters, the pronunciation expressed by 
the text in some other writing system.

For example;
>>>d = Unidecoder()
>>>d.decode(u"\u5317\u4EB0")
'Bei Jing'.
d = Unidecoder(lang='ja')
>>>d.decode(u"\u5317\u4EB0")
'Pe King'
      """,
      author='Hioshi Miura',
      author_email='miurahr@linux.com',
      packages = ['unihandecode',
                  'unihandecode.pykakasi',
                  'unihandecode.genkanwadict',
                  'unihandecode.gencodemap'],
      include_package_data = True,
      package_data = {'unihandecode':  ['*.pickle.bz2',
                                        'pykakasi/*.pickle',
                                        'pykakasi/kanwadict2.*']},
      provides = [ 'unihandecode' ],
      test_suite = 'nose.collector',
      cmdclass = {'build':my_build}
)
