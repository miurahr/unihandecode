#!/usr/bin/python
import os
import sys

from setuptools import setup
from setuptools.command.build_py import build_py

sys.path.insert(1, os.path.abspath(os.path.dirname(__file__)))
import unihandecode.gencodemap as gencodemap


class MyBuild(build_py):

    SUPPORTED_LANG = ['kr', 'ja', 'zh', 'vn', 'yue']

    def gen_map(self):
        unihan_source = os.path.join('unihandecode','data','Unihan_Readings.txt')
        for lang in self.SUPPORTED_LANG:
            dest = os.path.join('unihandecode',lang+'codepoints.pickle')
            u = gencodemap.UnihanConv(lang)
            u.run(source = unihan_source, dest=dest)

    def run(self):
        u = gencodemap.Unicodepoints()
        u.run(os.path.join('unihandecode','unicodepoints.pickle'))
        self.gen_map()
        build_py.run(self)


setup(cmdclass = {'build_py': MyBuild},
      use_scm_version={"local_scheme": "no-local-version"},
      setup_requires=['setuptools-scm>=3.5.0', 'setuptools>=42'])
