#!/bin/sh
make clean
make PYTHON=/usr/bin/python2 test
make PYTHON=/usr/bin/python2 bdist
make sdist
make PYTHON=python3 test 
make PYTHON=python3 bdist
