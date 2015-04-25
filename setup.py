#!/usr/bin/python
# derivered from unidecode setup.py

from setuptools import Command, setup, find_packages
from distutils.command.install import install as _install

import unittest
import os,threading
import sys
import unihandecode.gencodemap as gencodemap
import unihandecode.genkanwadict as genkanwadict


class genmap_t(threading.Thread):
    l = None
    def __init__(self, lang):
        threading.Thread.__init__(self)
        self.l = lang

    def run(self):
        unihan_source = os.path.join('data','Unihan_Readings.txt')
        dest = os.path.join('unihandecode',self.l+'codepoints.pickle')
        u = gencodemap.UnihanConv(self.l)
        u.run(source = unihan_source, dest=dest)

def genDict(src_f, pkl_f):
    kanwa = genkanwadict.mkkanwa()
    src = os.path.join('unihandecode','data',src_f)
    dst = os.path.join('unihandecode','pykakasi',pkl_f)
    try:
        os.unlink(dst)
    except:
        pass
    kanwa.mkdict(src, dst)

def _pre_install(dir):
    DICTS = [
        ('itaijidict.utf8', 'itaijidict2.pickle'),
        ('kanadict.utf8', 'kanadict2.pickle'),
    ]

    for (s,p) in DICTS:
        genDict(s, p)

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
    k= genmap_t('kr')
    j= genmap_t('ja')
    c= genmap_t('zh')
    v= genmap_t('vn')
    k.start()
    j.start()
    c.start()
    v.start()
    k.join()
    j.join()
    c.join()
    v.join()

def _post_install(dir):
    pass

class install(_install):
    def run(self):
        self.execute(_pre_install,  (self.install_lib,),
                    msg="Running pre install task")
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                    msg="Running post install task")

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
      package_data = {'unihandecode.data': ['*.utf8','*.txt']},
      provides = [ 'unihandecode' ],
      test_suite = 'nose.collector',
      cmdclass = {'install':install}

)
