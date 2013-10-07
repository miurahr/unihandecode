#!/bin/sh
rm -f unihandecode/*.pickle
rm -f unihandecode/pykakasi/*.pickle
rm -f unihandecode/pykakasi/*.db
python2 setup.py genmap
python2 setup.py gendict
python2 setup.py bdist_egg sdist
python3 setup.py gendict
python3 setup.py bdist_egg
