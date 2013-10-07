#!/usr/bin/python
# derivered from unidecode setup.py

from setuptools import Command,setup, find_packages

import unittest
import os,threading
import gencodemap
import genkanwadict

UNITTESTS = [
        "tests", 
    ]

class TestCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        suite = unittest.TestSuite()

        suite.addTests( 
            unittest.defaultTestLoader.loadTestsFromNames( 
                                UNITTESTS ) )

        result = unittest.TextTestRunner(verbosity=2).run(suite)


class GenKanwa(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def genDict(self, src_f, pkl_f):
        kanwa = genkanwadict.mkkanwa()
        src = os.path.join('data',src_f)
        dst = os.path.join('unihandecode','pykakasi',pkl_f)
        try:
            os.unlink(dst)
        except:
            pass
        kanwa.mkdict(src, dst)

    def run(self):

        DICTS = [
            ('itaijidict.utf8', 'itaijidict2.pickle'),
            ('kanadict.utf8', 'kanadict2.pickle'),
        ]

        for (s,p) in DICTS:
            self.genDict(s, p)

# kanwadict 
        src = os.path.join('data','kakasidict.utf8')    
        dst = os.path.join('unihandecode','pykakasi','kanwadict2') # don't add .db ext
        try:
            os.unlink(dst+'.db')
        except:
            pass
        kanwa = genkanwadict.mkkanwa()
        kanwa.run(src, dst)


class GenMap(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
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


setup(name='Unihandecode',
      version='0.42',
      description='US-ASCII transliterations of Unicode text',
      url='http://launchpad.net/unihandecode/',
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

      packages = find_packages(),
      include_package_data = True,
      package_data = {'unihandecode': ['*.pickle',
                                       'pykakasi/*.pickle',
                                       'pykakasi/*.db']},
      provides = [ 'unihandecode' ],

      cmdclass = { 'test': TestCommand,  'genmap':GenMap, 'gendict':GenKanwa }

)
