# Makefile for Unihandecode
# --*-- Makefile --*--
#

PYTHON=/usr/bin/python

# data directories
LROOT=unihandecode
DROOT=$(LROOT)/localedata
KROOT=$(LROOT)/pykakasi

# definitions
PKLS=$(DROOT)/jacodepoints.pickle $(DROOT)/zhcodepoints.pickle \
     $(DROOT)/vncodepoints.pickle $(DROOT)/krcodepoints.pickle \
     $(DROOT)/unicodepoints.pickle
DATASRC=data/UnicodeData.txt gencodemap/unicodepoints.py
KANWADICT=$(KROOT)/kanwadict2.dir $(KROOT)/kanwadict2.bak \
          $(KROOT)/kanwadict2.dat
KANWASRC=data/kakasidict.utf8
GLCP=gentable/glcp.py
TTBLS=$(DROOT)/de_DE.ttbl.bz2
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
	rm -f $(DROOT)/*.pickle
	rm -f $(DROOT)/*.ttbl.bz2
	rm -f $(LROOT)/*.pyc
	rm -f $(KROOT)/*.pickle
	rm -f $(KROOT)/kanwadict2.*
	rm -f $(KROOT)/*.pyc
	rm -rf build

# dictionaries/tables

$(PKLS): $(DATASRC)
	$(PYTHON) setup.py genmap

$(KANWADICT): $(KANWASRC)
	$(PYTHON) setup.py gendict

$(DROOT)/%.ttbl.bz2: $(TTBL_SRC_DIR)/%
	$(GLCP) --output-dir=$(DROOT) $<

