#!/usr/bin/python
# derivered from unidecode setup.py

from setuptools import Command, setup, find_packages
from setuptools.command.install import install
from distutils.command.build import build

import os,threading
import sys
import shutil
import unihandecode.gencodemap as gencodemap

SUPPORTED_LANG=['kr','ja','zh','vn','yue']

def gen_map():
    unihan_source = os.path.join('unihandecode','data','Unihan_Readings.txt')
    for lang in SUPPORTED_LANG:
        dest = os.path.join('unihandecode',lang+'codepoints.pickle')
        u = gencodemap.UnihanConv(lang)
        u.run(source = unihan_source, dest=dest)

def catdict(src_a, dst):
    outdict    = open(dst,'wb')
    for src_f in src_a:
      shutil.copyfileobj(open(os.path.join('unihandecode','data',src_f),'rb'), outdict)
    outdict.close()

def pre_build():
    u = gencodemap.Unicodepoints()
    u.run(os.path.join('unihandecode','unicodepoints.pickle'))
    gen_map()

class my_build(build):
    def run(self):
        self.execute(pre_build, (),
                    msg="Running pre build task")
        build.run(self)

class my_install(install):
    def run(self):
        self.execute(pre_build, (),
                    msg="Running pre build task")
        install.run(self) # run normal build command

tests_require = ['nose','coverage','mock']
if sys.version_info < (2, 7):
    tests_require.append('unittest2')

setup(name='Unihandecode',
      version='0.80',
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
                  'unihandecode.gencodemap'],
      include_package_data = True,
      package_data = {'unihandecode':  ['*.pickle.bz2']},
      provides = [ 'unihandecode' ],
      test_suite = 'nose.collector',
      tests_require = tests_require,
      cmdclass = {
          #'install':my_install,
          'build':my_build}
)
