# -*- coding: utf-8 -*-
#  kakasi.py
#
# Copyright 2011 Hiroshi Miura <miurahr@linux.com>
#
#  Original Copyright:
# * KAKASI (Kanji Kana Simple inversion program)
# * $Id: jj2.c,v 1.7 2001-04-12 05:57:34 rug Exp $
# * Copyright (C) 1992
# * Hironobu Takahashi (takahasi@tiny.or.jp)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either versions 2, or (at your option)
# * any later version.
# *
# * This program is distributed in the hope that it will be useful
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with KAKASI, see the file COPYING.  If not, write to the Free
# * Software Foundation Inc., 59 Temple Place - Suite 330, Boston, MA
# * 02111-1307, USA.
# */

import re
import sys, os
from .j2a import J2a
from .h2a import H2a
from .k2a import K2a

class kakasi(object):

    _conv = {}

    def __init__(self):
        self._conv["j"] = J2a()
        self._conv["h"] = H2a() 
        self._conv["k"] = K2a()
        return

    def do(self, text):
        otext =  ''
        i = 0
        while True:
            if i >= len(text):
                break

            if self._conv["j"].isRegion(text[i]):
                (t, l) = self._conv["j"].convert(text[i:])
                if l <= 0:
                    i = i + 1
                    continue
                i = i + l
                if i >= len(text):
                    otext = otext + t.capitalize()
                else:
                    otext = otext + t.capitalize() + ' '
 
            elif self._conv["h"].isRegion(text[i]):
                tmptext = ''
                while True:
                    (t, l) = self._conv["h"].convert(text[i:])
                    tmptext = tmptext+t
                    i = i + l
                    if i >= len(text):
                        otext = otext + tmptext                    
                        break
                    elif not self._conv["h"].isRegion(text[i]):
                        otext = otext + tmptext + ' '
                        break
            elif self._conv["k"].isRegion(text[i]):
                tmptext = ''
                while True:
                    (t, l) = self._conv["k"].convert(text[i:])
                    tmptext = tmptext+t
                    i = i + l
                    if i >= len(text):
                        otext = otext + tmptext                    
                        break
                    elif not self._conv["k"].isRegion(text[i]):
                        otext = otext + tmptext + ' '
                        break
            else:
                otext  = otext + text[i]
                i += 1

        return otext

