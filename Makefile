hancodepoints.py: genhancodemap/unihan_kconv.py 
	cd genhancodemap;\
	python unihan_kconv.py > ../unihandecode/hancodepoints.py
