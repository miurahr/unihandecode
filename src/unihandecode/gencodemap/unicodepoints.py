#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
import json

from typing import Dict, Optional

"""
Unicode code point dictionary generation for str.translate method.

Based on Text::Unidecode's xAB.pm lists. This combines all xAB.pm files into
a single dictionary.
"""


class Unicodepoints:
    def __init__(self):
        self.tbl = {}  # type: Dict[int, Optional[str]]
        with open(os.path.join(os.path.dirname(__file__), 'codepoint.json'), 'r') as f:
            codepoints = json.load(f)
            for high_byte in sorted(codepoints.keys()):
                for i, s in enumerate(codepoints[high_byte]):
                    assert i < 256
                    self.tbl[int(high_byte, 16) * 256 + i] = s

    def run(self, dest):
        with open(dest, 'wb') as outfile:
            pickle.dump(self.tbl, outfile)
