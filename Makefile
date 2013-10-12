

PYTHON=/usr/bin/python

all: test bdist sdist

test: genmap gendict
	$(PYTHON) setup.py test

genmap: unihandecode/*.pickle

gendict: unihandecode/pykakasi/kanwadict2.dir

bdist: genmap gendict
	$(PYTHON) setup.py bdist_egg

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -f unihandecode/*.pickle
	rm -f unihandecode/*.pyc
	rm -f unihandecode/pykakasi/*.pickle
	rm -f unihandecode/pykakasi/kanwadict2.*
	rm -f unihandecode/pykakasi/*.pyc

stamp-genmap:
	touch stamp-genmap

unihandecode/*.pickle: data/UnicodeData.txt
	$(PYTHON) setup.py genmap

unihandecode/pykakasi/kanwadict2.dir: data/kakasidict.utf8
	$(PYTHON) setup.py gendict
