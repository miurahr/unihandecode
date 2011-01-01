#!/usr/bin/env python
import anydbm
import re, sys
import marshal

records = {}
for line in open("kakasidict.utf8", "r"):
    line = line.decode("utf-8").strip()
    if re.match(r'^;;', line): # skip comment
        continue
    (yomi, kanji) = line.strip().split(' ')
    key = "%04x"%ord(kanji[0])
    m = re.match('[a-z]',yomi[-1:]) 
    if m is not None:
        tail = yomi[-1:]
        yomi = yomi[:-1]
    else:
        tail = ''
    if records.has_key(key):
        records[key][kanji]=(yomi, tail)
    else:
        records[key] = {}
        records[key][kanji]=(yomi, tail)
        
dic = anydbm.open("kanwadict2.db", 'c')
for (k, v) in records.iteritems():
    dic[k] = marshal.dumps(v)
dic.close()
