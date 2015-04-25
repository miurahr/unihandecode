# Makefile for Unihandecode
# --*-- Makefile --*--
#

PYTHON=/usr/bin/env python

# definitions
PKLBZS=unihandecode/jacodepoints.pickle.bz2 unihandecode/zhcodepoints.pickle.bz2 \
     unihandecode/vncodepoints.pickle.bz2 unihandecode/krcodepoints.pickle.bz2 \
     unihandecode/unicodepoints.pickle.bz2
DATASRC=unihandecode/data/UnicodeData.txt unihandecode/gencodemap/unicodepoints.py
KANWADICT=unihandecode/pykakasi/kanwadict2.dir unihandecode/pykakasi/kanwadict2.bak \
          unihandecode/pykakasi/kanwadict2.dat
KANWASRC=unihandecode/data/kakasidict.utf8

all: test bdist sdist

# build targets

install: build
	$(PYTHON) setup.py install

test: build
	nosetests

dist: bdist sdist

bdist: build
	$(PYTHON) setup.py bdist_wheel

sdist:
	$(PYTHON) setup.py sdist

build: $(DATASRC) $(KANWASRC)
	$(PYTHON) setup.py build

# clean target

dist-clean: clean
	rm -rf dist

clean:
	$(PYTHON) setup.py clean
	rm -f $(PKLBZS)
	rm -f $(KANWADIT)
	rm -f unihandecode/pykakasi/*.pickle
	rm -f unihandecode/pykakasi/*.pyc
	rm -f unihandecode/*.pyc
	rm -rf build
	find . -name '*~' -exec rm -f {} \;
