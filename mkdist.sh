#!/bin/sh
rm -f unihandecode/*.pickle
rm -f unihandecode/pykakasi/*.pickle
rm -f unihandecode/pykakasi/kanwadict2.*
python2 setup.py genmap
python2 setup.py gendict
python2 setup.py sdist bdist_egg
rm -f unihandecode/pykakasi/kanwadict2.*
python3 setup.py gendict
python3 setup.py bdist_egg
