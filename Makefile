# Makefile for Unihandecode
# --*-- Makefile --*--
#

PYTHON=/usr/bin/python

# definitions
PKLS=unihandecode/jacodepoints.pickle unihandecode/zhcodepoints.pickle \
     unihandecode/vncodepoints.pickle unihandecode/krcodepoints.pickle \
     unihandecode/unicodepoints.pickle
DATASRC=data/UnicodeData.txt gencodemap/unicodepoints.py
KANWADICT=unihandecode/pykakasi/kanwadict2.dir unihandecode/pykakasi/kanwadict2.bak \
          unihandecode/pykakasi/kanwadict2.dat
KANWASRC=data/kakasidict.utf8
GLCP=gentable/glcp.py
TTBLS=unihandecode/de_DE.ttbl.bz2
TTBL_SRC_DIR=/usr/share/i18n/locales

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

genmap: $(PKLS) $(TTBLS)

gendict: $(KANWADICT)

# clean target

dist-clean: clean
	rm -rf dist
clean:
	rm -f unihandecode/*.pickle
	rm -f unihandecode/*.pyc
	rm -f unihandecode/pykakasi/*.pickle
	rm -f unihandecode/pykakasi/kanwadict2.*
	rm -f unihandecode/pykakasi/*.pyc
	rm -rf build

# dictionaries/tables

$(PKLS): $(DATASRC)
	$(PYTHON) setup.py genmap

$(KANWADICT): $(KANWASRC)
	$(PYTHON) setup.py gendict

unihandecode/%.ttbl.bz2: $(TTBL_SRC_DIR)/%
	$(GLCP) --output-dir=unihandecode/ $<

