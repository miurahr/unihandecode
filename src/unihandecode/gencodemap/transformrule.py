import re
import xml.etree.ElementTree as ET
from typing import Dict, Optional


class TransformRule:

    def __init__(self, lang: str):
        self.lang = lang
        self.tbl = {}  # type: Dict[int, Optional[str]]

    def load(self, filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        for tr in root.iter("transform"):
            for rule in tr.iter("tRule"):
                self.text = rule.text
                self._parse()
                return

    @classmethod
    def from_string(cls, lang: str, text: str):
        obj = cls(lang)
        obj.text = text
        obj._parse()
        return obj

    def _parse(self):
        r0 = re.compile(r"^(\S+)\s?→\s?(\S+)\s?;.*$")
        for line in self.text.splitlines():
            if line.startswith("#"):
                continue
            m = r0.match(line)
            if m is not None:
                self.tbl[m.group(1)] = m.group(2).encode().decode('unicode-escape')

    def as_dictionary(self):
        return self.tbl
