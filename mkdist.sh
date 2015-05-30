#!/bin/sh
make clean
make sdist
make test
make bdist
