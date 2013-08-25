#!/bin/sh
python2 setup.py genmap
python2 setup.py gendict
python2 setup.py bdist_egg
python3 setup.py genmap
python3 setup.py gendict
python3 setup.py bdist_egg
