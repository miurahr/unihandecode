# Makefile for Unihandecode
# --*-- Makefile --*--
#

PYTHON=/usr/bin/env python

# definitions
PKLBZS=unihandecode/jacodepoints.pickle.bz2 unihandecode/zhcodepoints.pickle.bz2 \
     unihandecode/vncodepoints.pickle.bz2 unihandecode/krcodepoints.pickle.bz2 \
     unihandecode/unicodepoints.pickle.bz2
DATASRC=data/UnicodeData.txt gencodemap/unicodepoints.py
KANWADICT=unihandecode/pykakasi/kanwadict2.dir unihandecode/pykakasi/kanwadict2.bak \
          unihandecode/pykakasi/kanwadict2.dat
KANWASRC=data/kakasidict.utf8

all: test bdist sdist

# build targets

install: genmap gendict
	$(PYTHON) setup.py install

test: genmap gendict
	nosetests -v

dist: bdist sdist

bdist: genmap gendict
	$(PYTHON) setup.py bdist_egg

sdist:
	$(PYTHON) setup.py sdist

genmap: $(PKLBZS)

gendict: $(KANWADICT)

# clean target

dist-clean: clean
	rm -rf dist
clean:
	$(PYTHON) setup.py clean
	rm -f unihandecode/*.pyc
	rm -f unihandecode/*.pickle.bz2
	rm -f unihandecode/*.pickle
	rm -f unihandecode/pykakasi/*.pickle
	rm -f unihandecode/pykakasi/*.pyc
	rm -f unihandecode/pykakasi/kanwadict2.*
	rm -rf build
	find . -name '*~' -exec rm -f {} \;

# dictionaries

$(PKLBZS): $(DATASRC)
	$(PYTHON) setup.py genmap

$(KANWADICT): $(KANWASRC)
	$(PYTHON) setup.py gendict

