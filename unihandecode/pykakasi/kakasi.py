# -*- coding: utf-8 -*-
#  kakasi.py
#
# Copyright 2011,2014 Hiroshi Miura <miurahr@linux.com>
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
from .k2a import K2a

class kakasi(object):

    _conv = {}
    _separator = ' '
    _endmark = [0x002c, 0x002e, 0x3001, 0x3002]

    def __init__(self):
        self._conv["j"] = J2a()
        self._conv["k"] = K2a()
        return

    def do(self, text):
        otext =  ''
        i = 0
        while True:
            if i >= len(text):
                break

            if self._conv["j"].canConvert(text[i]):
                (t, l) = self._conv["j"].convert(text[i:])
                if l <= 0:
                    # XXX: problem happens.
                    i += 1
                    continue
                i = i + l
                otext = otext + t.capitalize()
                # Not insert space BEFORE end marks and text end.
                if (i < len(text)) and not (ord(text[i]) in self._endmark):
                    otext = otext + self._separator
 
            elif self._conv["k"].canConvert(text[i]):
                while True:
                    (t, l) = self._conv["k"].convert(text[i:])
                    # when fails to convert it return ("", -1)
                    # at first detect it.
                    if l <= 0:
                        # XXX: problem happens.
                        #  come here when character text[i] is
                        #  inside range where claming enable to
                        #  convert with _conv["k"] converter.
                        #  but conversion was failed.
                        #  In order to recover it, skip text[i] and ignored.
                        i  += 1
                        continue
                    i = i + l
                    otext = otext + t
                    if i >= len(text): # finished
                        break
                    elif not self._conv["k"].canConvert(text[i]):
                        # Found a place _conv["k"] cannot convert.
                        # this means we found word boundary.
                        # Inserting word separator(space) to indicate word boundary.
                        # Not inserting space BEFORE comma and full stop
                        if not ord(text[i]) in self._endmark:
                            otext = otext + self._separator
                        break
                    else:
                        # We can process next character with _conv["k"]
                        # treat it is connected previous convertion
                        # in means of word boundary.
                        pass
            else:
                otext  = otext + text[i]
                i += 1

        return otext

