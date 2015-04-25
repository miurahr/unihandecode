#!/bin/sh
make clean
make sdist
make PYTHON=python2 test
make PYTHON=python2 bdist
make clean
make PYTHON=python3 test 
make PYTHON=python3 bdist
make clean
