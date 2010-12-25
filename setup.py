#!/usr/bin/python
# derivered from unidecode setup.py

from distutils.core import Command, setup
from distutils.command.install import install as DistutilsInstall
import genhancodemap
import unittest

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

class Installer(DistutilsInstall):
    def run(self):
        #do_pre_install_staff()
        DistutilsInstall.run(self)
        #do_post_install_staff()

class GenMap(Object):
    def run(self,lang='korean'):
        if lang=='korean':
            genhancodemap.unihan_kconv('genhancodemap/Unihan_Readings.txt')



setup(name='Unihandecode',
      version='0.01',
      description='US-ASCII transliterations of Unicode text',
      url='http://launchpad.net/unihandecode/',
      license='GPLv3',
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

For example 'decode(u"\u5317\u4EB0")' returns 'Bei Jing'.

      """,
      author='Hioshi Miura',
      author_email='miurahr@linux.com',

      packages = [ 'unihandecode' ],

      provides = [ 'unihandecode' ],

      cmdclass = { 'test': TestCommand, 'install':Installer, 'genmap':GenMap }
)
