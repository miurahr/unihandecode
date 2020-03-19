import os
import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def dictionary_setup_fixture():
    if "TOX_ENV_DIR" not in os.environ:
        root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(1, os.path.join(root_dir, 'src'))
        import unihandecode.gencodemap as gencodemap
        dpath = os.path.join(root_dir, 'build', 'lib', 'unihandecode')
        os.makedirs(dpath, exist_ok=True)
        dest = os.path.join(dpath, 'unicodepoints.pickle')
        u = gencodemap.Unicodepoints()
        u.run(dest)
        unihan_source = os.path.join(root_dir, 'src', 'unihandecode', 'data', 'Unihan_Readings.txt')
        SUPPORTED_LANG = ['kr', 'ja', 'zh', 'vn', 'yue']
        for lang in SUPPORTED_LANG:
            dest = os.path.join(dpath, lang + 'codepoints.pickle')
            u = gencodemap.UnihanConv(lang)
            u.run(source=unihan_source, dest=dest)
        from unihandecode import Configurations
        Configurations()._data_path = dpath
