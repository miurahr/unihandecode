#!/usr/bin/python
import os
import sys

from setuptools import setup
from setuptools.command.build_py import build_py


class MyBuild(build_py):

    def pre_build(self):
        sys.path.insert(1, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src'))
        import unihandecode.gencodemap as gencodemap
        os.makedirs(os.path.join(self.build_lib, 'unihandecode', 'data'), exist_ok=True)
        dest = os.path.join(self.build_lib, 'unihandecode', 'data', 'unicodepoints.pickle')
        u = gencodemap.Unicodepoints()
        u.run(dest)
        unihan_source = os.path.join('src', 'unihandecode', 'data', 'Unihan_Readings.txt')
        SUPPORTED_LANG = ['kr', 'ja', 'zh', 'vn', 'yue']
        for lang in SUPPORTED_LANG:
            dest = os.path.join(self.build_lib, 'unihandecode', 'data', lang + 'codepoints.pickle')
            u = gencodemap.UnihanConv(lang)
            u.run(source=unihan_source, dest=dest)

    def run(self):
        self.execute(self.pre_build, (), msg="Running pre build task")
        build_py.run(self)


setup(cmdclass={'build_py': MyBuild},
      use_scm_version={"local_scheme": "no-local-version"},
      setup_requires=['setuptools-scm>=3.5.0', 'setuptools>=42', 'wheel', 'pykakasi>=2.0.0a5'])
