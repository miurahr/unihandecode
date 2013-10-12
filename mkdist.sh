#!/bin/sh
make clean
make sdist
make PYTHON=/usr/bin/python2 test
make PYTHON=/usr/bin/python2 bdist
make PYTHON=/usr/bin/python3 test 
make PYTHON=/usr/bin/python3 bdist
