#!/bin/sh
make clean
make sdist
make PYTHON=c:\Python27\bin\python test
make PYTHON=c:\Python27\bin\python bdist
make clean
make PYTHON=c:\Python33\bin\python test 
make PYTHON=c:\Python33\bin\python bdist
