#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pickle
from typing import Dict, Optional, Tuple


class UnihanConv:

    readings = {}  # type: Dict[str, Tuple[str, int]]
    firsttime = True
    lang = None
    priority = {
        "kr": ["kKorean", "kMandarin", "kJapaneseOn", "kVietnamese", "kCantonese", "kJapaneseKun"],
        "zh": ["kMandarin", "kCantonese", "kKorean", "kJapaneseOn", "kVietnamese", "kJapaneseKun"],
        "yue": ["kCantonese", "kMandarin", "kKorean", "kJapaneseOn", "kVietnamese", "kJapaneseKun"],
        "ja": ["kJapaneseOn", "kJapaneseKun", "kMandarin", "kCantonese", "kKorean", "kVietnamese"],
        "vn": ["kVietnamese", "kMandarin", "kCantonese", "kJapaneseOn", "kJapaneseKun", "kKorean"],
    }
    pronounce_char_map = {
        "â": "a",
        "à": "a",
        "ắ": "a",
        "ă": "a",
        "ấ": "a",
        "ü": "u",
        "ụ": "u",
        "ú": "u",
        "ử": "u",
        "ư": "u",
        "ù": "u",
        "é": "e",
        "ọ": "o",
        "ố": "o",
        "ộ": "o",
        "ơ": "o",
        "ớ": "o",
    }

    def __init__(self, lang):
        self.tbl = {}  # type: Dict[int, Optional[str]]
        self.prio = {}  # type: Dict[int, int]
        if lang in self.priority:
            self.lang = lang
        else:
            self.lang = "zh"

    def run(self, source, dest):
        with open(source, "r", encoding="utf8") as f:
            self.process_file(f)
        with open(dest, "wb") as outfile:
            pickle.dump(self.tbl, outfile)

    def process_file(self, f):
        # Retrive U+XXXX from a first of line in a definition
        # for example;
        # U+3432	kMandarin	DAI4
        # r1 is a expression to get U+<char code>
        r1 = re.compile(r"U\+([0-9A-F]{4,5})\b")
        for line in f:
            items = line[:-1].split("\t")
            try:
                code = int(r1.sub(r"\1", items[0]), 16)
                category = items[1]
                try:
                    p = self.priority[self.lang].index(category)
                except:
                    continue
                if (code not in self.prio) or ( p < self.prio[code]):
                    self.prio[code] = p
                    pron = re.sub("[^\00-\x7f]", lambda x: self.pronounce_char_map[x.group()], items[2].split(" ")[0]).capitalize()
                    if category in ["kMandarin", "kCantonese"]:
                        self.tbl[code] = re.sub(r"(\w+)[1-5]", r"\1 ", pron)
                    elif category == "kHanyuPinyin":  # pragma: no branch
                        self.tbl[code] = re.sub(r"\w+\.\w+:(\w+)", r"\1 ", pron)  # pragma: no cover
                    else:
                        self.tbl[code] = "%s " % pron
            except:
                continue
