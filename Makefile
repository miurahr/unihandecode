# Makefile for Unihandecode
# --*-- Makefile --*--
#

PYTHON=/usr/bin/python

# definitions
PKLS=unihandecode/jacodepoints.pickle unihandecode/zhcodepoints.pickle \
     unihandecode/vncodepoints.pickle unihandecode/krcodepoints.pickle \
     unihandecode/unicodepoints.pickle
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
	$(PYTHON) setup.py test

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
	rm -f unihandecode/*.pickle.bz2
	rm -f unihandecode/*.pickle
	rm -f unihandecode/*.pyc
	rm -f unihandecode/pykakasi/*.pickle
	rm -f unihandecode/pykakasi/kanwadict2.*
	rm -f unihandecode/pykakasi/*.pyc
	rm -rf build

# dictionaries

$(PKLS): $(DATASRC)
	$(PYTHON) setup.py genmap

$(KANWADICT): $(KANWASRC)
	$(PYTHON) setup.py gendict

%.pickle.bz2: %.pickle
	bzip2 -kf $<
