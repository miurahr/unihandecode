#!/usr/bin/env python
# coding:utf8

from kandecoder import Kandecoder
from handecoder import Handecoder
from unidecoder import Unidecoder

from unihandecode import Unihandecoder

u = Unidecoder()
k = Kandecoder()
h = Handecoder()

print u.decode(u"明天明天的风吹")
print k.decode(u"明日は明日の風が吹く")
print h.decode(u"내일은 내일 바람이 분다")

uh = Unihandecoder(encoding="utf-8",lang="ch")
print uh.decode(u"明天明天的风吹")
uh = Unihandecoder(encoding="utf-8",lang="ja")
print uh.decode(u"明日は明日の風が吹く")
uh = Unihandecoder(encoding="utf-8",lang="ch")
print uh.decode(u"내일은 내일 바람이 분다")

"""
result should be:

Ashita ha Ashita no Kaze ga Fuku
Ming Tian Ming Tian De Feng Chui 
naeileun naeil barami bunda
"""

