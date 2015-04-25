#!/usr/bin/python
# derivered from unidecode setup.py

from setuptools import Command, setup, find_packages
from distutils.command.build import build

import unittest
import os,threading
import sys
import shutil
import unihandecode.gencodemap as gencodemap
import unihandecode.genkanwadict as genkanwadict

SUPPORTED_LANG=['kr','ja','zh','vn']

def gen_map():
    unihan_source = os.path.join('unihandecode','data','Unihan_Readings.txt')
    for lang in SUPPORTED_LANG:
        dest = os.path.join('unihandecode',lang+'codepoints.pickle')
        u = gencodemap.UnihanConv(lang)
        u.run(source = unihan_source, dest=dest)

def gen_dict(src, dst):
    kanwa = genkanwadict.mkkanwa()
    try:
        os.unlink(dst)
    except:
        pass
    kanwa.mkdict(src, dst)

def catdict(src_a, dst):
    outdict    = open(dst,'wb')
    for src_f in src_a:
      shutil.copyfileobj(open(os.path.join('unihandecode','data',src_f),'rb'), outdict)
    outdict.close()

def gen_kanwa(src, dst):
    try:
        os.unlink(dst+'.db')
    except:
        pass
    kanwa = genkanwadict.mkkanwa()
    kanwa.run(src, dst)

def _pre_build():
    # build itaijidict
    src = os.path.join('unihandecode','data','itaijidict.utf8')
    dst = os.path.join('unihandecode','pykakasi','itaijidict2.pickle')
    gen_dict(src, dst)

    # build kanadict
    #catdict(['kanadict.utf8','gairaidict.utf8','ryakugodict.utf8'], os.path.join('/tmp','kanadict2.utf8'))
    # ad-hoc fix... igore it; gairai word should treat as same as kanwadict, not as kana dict
    #  kana dict is basically one by one pronounce mapping, but gairai word is not; need spacing.
    catdict(['kanadict.utf8','ryakugodict.utf8'], os.path.join('/tmp','kanadict2.utf8'))
    src = os.path.join('/tmp','kanadict2.utf8')
    dst = os.path.join('unihandecode','pykakasi','kanadict2.pickle')
    gen_dict(src, dst)
    os.unlink(os.path.join('/tmp','kanadict2.utf8'))

    # build kakasi dict
    src = os.path.join('unihandecode','data','kakasidict.utf8')
    dst = os.path.join('unihandecode','pykakasi','kanwadict2') # don't add .db ext
    gen_kanwa(src, dst)

    # build unicode maps
    u = gencodemap.Unicodepoints()
    u.run(os.path.join('unihandecode','unicodepoints.pickle'))
    gen_map()

class my_build(build):
    def run(self):
        self.execute(_pre_build, (),
                    msg="Running pre build task")
        build.run(self)

setup(name='Unihandecode',
      version='0.50',
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
