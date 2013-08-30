#!/usr/bin/env python
# coding=utf8

from logbook import Logger

from exc import ParserError

class BaseParser(object):
    @property
    def lineno(self):
        return self.tokenizer.lineno

    @property
    def colno(self):
        return self.tokenizer.colno

    def _expect(self, *args):
        t = self.tokens.next()
        if not args == t[:len(args)]:
            raise ParserError(self, 'Expected %s, got %s instead' % \
                (args, t)
            )
        return t


class BlockParser(BaseParser):
    BLOCK_TYPES = ['LC_IDENTIFICATION', 'LC_CTYPE', 'LC_COLLATE', 'LC_TIME',
                   'LC_NUMERIC', 'LC_MONETARY', 'LC_MESSAGES', 'LC_PAPER',
                   'LC_NAME', 'LC_ADDRESS', 'LC_TELEPHONE']
    log = Logger('BlockParser')

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokens = iter(self.tokenizer)

    def parse(self):
        def _yield_until_end_of(blocktype):
            prev = None
            while True:
                t = self.tokens.next()
                if ('KEYWORD', 'END') == t and ('EOL',) == prev:
                    self._expect('KEYWORD', blocktype)
                    self._expect('EOL')
                    # done with the section
                    raise StopIteration

                yield t
                prev = t

        for t in self.tokens:
            if t[0] == 'KEYWORD' and t[1] in self.BLOCK_TYPES:
                handler = getattr(self, 'handle_' + t[1], None)
                gen = _yield_until_end_of(t[1])

                if not handler:
                    for g in gen:
                        pass  # skip until end
                    self.log.debug('skipping %s' % t[1])
                else:
                    handler(gen)


class TranslitParser(BlockParser):
    log = Logger('TranslitParser')
    def __init__(self, parse_func, *args, **kwargs):
        super(TranslitParser, self).__init__(*args, **kwargs)
        self.parse_func = parse_func
        self.ttbl = {}

        self.has_LC_IDENITIFCATION = False

    def handle_LC_IDENTIFICATION(self, tokens):
        self.has_LC_IDENITIFCATION = True
        for t in tokens:
            pass

    def handle_LC_CTYPE(self, tokens):
        self.log.debug('enter LC_CTYPE')
        inside_translit = False
        token_iter = iter(tokens)
        for t in token_iter:
            if ('KEYWORD', 'copy') == t:
                if inside_translit:
                    raise ParserError(self, 'copy inside translit section')

                t_fn = token_iter.next()
                if not (t_fn[0], 'STRING'):
                    raise ParserError(self, 'expected filename to copy')

                fn = t_fn[1]
                self.log.info('copying file "%s"' % fn)
                self.ttbl.update(self.parse_func(fn))

                if not ('EOL',) == token_iter.next():
                    raise ParserError(self, 'garbage after copy')
                continue

            if ('KEYWORD', 'include') == t:
                if not inside_translit:
                    raise ParserError(self, 'include outside translit section')

                t_fn = token_iter.next()
                if not (t_fn[0], 'STRING'):
                    raise ParserError(self, 'expected filename to copy')

                fn = t_fn[1]
                self.log.info('including file "%s"' % fn)
                self.ttbl.update(self.parse_func(fn))

                while token_iter.next() != ('EOL',):
                    pass
                continue

            if ('KEYWORD', 'translit_start') == t:
                self.log.debug('enter translit')
                inside_translit = True
                continue

            if ('KEYWORD', 'translit_end') == t:
                self.log.debug('exit translit')
                inside_translit = False
                continue

            if ('KEYWORD', 'default_missing') == t:
                self.log.debug('skipping default_missing')
                while token_iter.next() != ('EOL',):
                    pass
                continue

            if inside_translit and t != ('EOL',):
                # "ordinary" translit line
                groups = []

                current_group = []
                while t != ('EOL',):
                    if ('SEMICOLON',) == t:
                        groups.append(current_group)
                        current_group = []
                        t = token_iter.next()
                        continue

                    if not 'STRING' == t[0]:
                        raise ParserError(self, 'string expected, found %r'\
                                                'instead' % (t,))
                    current_group.append(t[1])

                    t = token_iter.next()

                if current_group:
                    groups.append(current_group)

                if len(groups) == 1:
                    assert len(groups[0]) == 2
                    lhs = [groups[0][0]]
                    rhs = groups[0][1]
                elif len(groups) >= 2:
                    # last substition seems to be the simplest
                    lhs = groups[0]
                    rhs = groups[-1][0]

                    assert len(groups[-1]) == 1

                    if len(groups) > 2:
                        self.log.warning('Unhandled leftover substitutions: '\
                                         '%s' % groups)

                for l in lhs:
                    self.ttbl[l] = rhs


        if inside_translit:
            raise ParserError(self, 'translit_end not found')
        self.log.debug('exit LC_CTYPE')
