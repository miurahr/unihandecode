# Unihandecode

 [![travis-ci](https://secure.travis-ci.org/miurahr/unihandecode.png)](https://secure.travis-ci.org/miurahr/unihandecode)
 [![Downloads](https://pypip.in/d/Unihandecode/badge.png)](https://crate.io/package/Unihandecode)
 [![PyPI version](https://badge.fury.io/py/Unihandecode.png)](http://badge.fury.io/py/Unihandecode)

ASCII transliterations of Unicode text that recognize CJKV complex charactors


EXAMPLE USE
-----------

 You can run it on python interpreter(in 2.x):

        from unihandecode import Unihandecoder
        d = Unihandecoder(lang='zh')
        print d.decode(u"\u660e\u5929\u660e\u5929\u7684\u98ce\u5439")

        # That prints: Ming Tian Ming Tian De Feng Chui 

        u = Unihandecoder(lang='ja')
        print d.decode(
            u'\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f')

        # That prints: Ashita ha Ashita no Kaze ga Fuku

 There are some other examples in tests/basic_2.py.

 You can also learn from actual applications which use unihandecode, such as
 
 * calibre-ebook: https://github.com/kovidgoyal/calibre/tree/master/src/calibre/ebooks/unihandecode


DESCRIPTION
-----------

 It often happens that you have non-Roman text data in Unicode, but
 you can't display it -- usually because you're trying to show it
 to a user via an application that doesn't support Unicode, or
 because the fonts you need aren't accessible. You could represent
 the Unicode characters as "???????" or "\15BA\15A0\1610...", but
 that's nearly useless to the user who actually wants to read what
 the text says.

 What Unihandecode provides is a function, 'decode(...)' that
 takes Unicode data and tries to represent it in ASCII characters 
 (i.e., the universally displayable characters between 0x00 and 0x7F). 
 The representation is almost always an attempt at *transliteration* 
 -- i.e., conveying, in Roman letters, the pronunciation expressed by 
 the text in some other writing system. (See the example above)

 These are same meaning in both language in example above.
 "明天明天的风吹" for Chinese and "明日は明日の風が吹く" for Japanese.
 The character "明" is converted "Ming" in Chinese. "明日" is converted
 "Ashita" but single charactor "明" will be converted "Mei" in Japanese.

 This is an improved version of Python unidecode,
 that is Python port of Text::Unidecode Perl module by 
 Sean M. Burke <sburke@cpan.org>.

REQUIREMENTS
------------

 It use a setuptools library to build and test.


INSTALLATION
------------

 You install Unihandecode by running these commands:

        make clean
        make
        make install

 If you got egg package, it is easy to install by
 ```$ easy_install Unihandecode-0.42-py2.7.egg```

BUILD
------

 To build egg package;

        make dist

TEST
------

 To do unit test, run

        make test


LIMITATION
----------

 This library uses pickler that format is depend on platform
 and python version.
 You should re-create dictionary for each python version.
 To avoid a dependency problem, always recommend to run ```make clean```
 before build.

SUPPORT
--------

 Questions, bug reports, useful code bits, and suggestions for
 Unihandecode are handled on github.com/miurahr/unihandecode


AVAILABILITY
------------

 The latest version of Unihandecode is available from
 Git repository in github.com:

	https://github.com/miurahr/unihandecode

 and Eggs are on PyPi.python.org:
 
        https://pypi.python.org/pypi/Unihandecode

 WARNING: There was launchpad.net Bazzar repository named unhandecode.
 It has NOT been maintained and moved github entirely.


COPYRIGHT
---------

Unicode Character Database:
 Date: 2010-09-23 09:29:58 UDT [JHJ]
 Unicode version: 6.0.0

 Copyright (c) 1991-2010 Unicode, Inc.
 For terms of use, see http://www.unicode.org/terms_of_use.html
 For documentation, see http://www.unicode.org/reports/tr44/

Unidecode's character transliteration tables:

Copyright 2001, Sean M. Burke <sburke@cpan.org>, all rights reserved.

Python code:

Copyright 2010,2011, Hiroshi Miura <miurahr@linux.com>
Copyright 2009, Tomaz Solc <tomaz@zemanta.com>


LICENSE
-------

Unihandecode
     Copyright 2010-2013 Hiroshi Miura

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
