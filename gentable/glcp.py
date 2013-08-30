#!/usr/bin/env python
# coding=utf8

"""A script to extract glibc localedata.

Woefully under documented. All its components are found in the glibcparse
package. If you need a parser for glibc locale files for some reason, this is
not a bad starting point. Message me on <https://github.com/mbr/slugger> for
help.
"""

import bz2
import os
import sys

import logbook
import logbook.more

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from remember.memoize import memoize
    has_memoize = True
except ImportError:
    has_memoize = False

    def memoize(*args, **kwargs):
        def _wrap(f):
            return f
        return _wrap

from glibcparse.tokenize import Tokenizer
from glibcparse.preprocess import Screener
from glibcparse.parser import TranslitParser
from glibcparse.exc import LException

log = logbook.Logger('main')

def parse_translit(fn):
    return _parse_translit(os.path.normpath(os.path.abspath(fn)))

@memoize(100)
def _parse_translit(fn):
    with open(fn) as f:
        log.info("parse %s" % os.path.relpath(fn))
        tok = Tokenizer(Screener(f.read()))
        dirname = os.path.dirname(fn)

        def parse_func(new_fn):
            full_fn = os.path.join(dirname, new_fn)
            return parse_translit(full_fn)[0]

        p = TranslitParser(parse_func, tok)

        try:
            p.parse()
        except LException, e:
            log.critical("%s:%d.%d %s" % (
                fn,
                e.src.lineno,
                e.src.colno,
                e.err
            ))
            sys.exit(1)

        return p.ttbl, p


if '__main__' == __name__:
        import argparse
        parser = argparse.ArgumentParser(
            description="""Parses the provided files, calculates translation
                           tables and writes them as bzip'ed pickle files to
                           disc."""
        )
        parser.add_argument('files', metavar='FILE', nargs='+',
                            help="""localedata files to be parsed. Inside a
                            checkout of the glibc repository, these are usually
                            as [glibc]/localedata/locales/*""")
        parser.add_argument('--preprocess-only', '-E', action='store_true',
                            default=False, help="""Used to test comment
                            stripping and folding new lines.""")
        parser.add_argument('--debug', '-d', action='store_const',
                            dest='loglevel', const=logbook.DEBUG,
                            default=logbook.INFO, help="""Show debugging output
                            while working""")
        parser.add_argument('--output-dir', '-o',
                            default=os.path.join(
                                os.path.dirname(__file__),
                                'slugger/localedata'), help="""The directory
                            where generated output should be stored. Defaults
                            to slugger/localedata.""")
        parser.add_argument('--no-compression', '-C', dest='compress',
                            default=True, action='store_false', help="""Do not
                            compress resulting files.""")

        args = parser.parse_args()
        logbook.NullHandler().push_application()
        logbook.more.ColorizedStderrHandler(
            level=args.loglevel,
        ).push_application()

        if not has_memoize:
            log.error('You do not have remember (from PyPi) installed. This '\
                      'program will still work, but large jobs will run about'\
                      ' 10x slower')

        log.info('Storing output in %s' % args.output_dir)

        for fn in args.files:
            if args.preprocess_only:
                with open(fn) as f:
                    for c in Screener(f.read()):
                        sys.stdout.write(c)
            else:
                ttbl, parser = parse_translit(fn)
                if not parser.has_LC_IDENITIFCATION:
                    log.warning('No LC_IDENTIFICATION in "%s", skipping' %\
                                fn)
                else:
                    ext = '.ttbl' if not args.compress else '.ttbl.bz2'
                    out_fn = os.path.join(
                        args.output_dir,
                        os.path.basename(fn) + ext)
                    log.info('Writing output to %s' % out_fn)

                    outfile = open(out_fn, 'w') if not args.compress else\
                              bz2.BZ2File(out_fn, 'w', 1024**2, 9)
                    try:
                        pickle.dump(ttbl, outfile, pickle.HIGHEST_PROTOCOL)
                    finally:
                        outfile.close()
