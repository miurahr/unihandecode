#!/usr/bin/env python
import anydbm, marshal

class mkkanwa(object):

    records = {}

    def run(self, src, dst):
        for line in open(src, "r"):
            self.parsekdict(line)
        self.kanwaout(dst)

    def parsekdict(self, line):
        line = line.decode("utf-8").strip()
        if line.startswith(';;'): # skip comment
            return
        (yomi, kanji) = line.split(' ')
        if ord(yomi[-1:]) <= ord('z'): 
            tail = yomi[-1:]
            yomi = yomi[:-1]
        else:
            tail = ''
        self.updaterec(kanji, yomi, tail)

    def updaterec(self, kanji, yomi, tail):
            key = "%04x"%ord(kanji[0])
            if self.records.has_key(key):
                self.records[key][kanji]=(yomi, tail)
            else:
                self.records[key] = {}
                self.records[key][kanji]=(yomi, tail)
        
    def kanwaout(self, out):
        dic = anydbm.open(out, 'c')
        for (k, v) in self.records.iteritems():
            dic[k] = marshal.dumps(v)
        dic.close()
