============
Unihandecode
============

Overview
========

.. image:: https://github.com/miurahr/unihandecode/workflows/Run%20Tox%20tests/badge.svg
   :alt: GH-A: Tox tests
.. image:: https://secure.travis-ci.org/miurahr/unihandecode.png
   :target: https://secure.travis-ci.org/miurahr/unihandecode
   :alt: Travis-CI
.. image:: https://ci.appveyor.com/api/projects/status/pcguwvtvwc23g20v?svg=true
   :target: https://ci.appveyor.com/project/miurahr/unihandecode
   :alt: AppVeyor
.. image:: https://coveralls.io/repos/miurahr/unihandecode/badge.svg?branch=master
   :target: https://coveralls.io/r/miurahr/unihandecode?branch=master
   :alt: Coverage Status
.. image:: https://badge.fury.io/py/Unihandecode.png
   :target: http://badge.fury.io/py/Unihandecode
   :alt: PyPI version

ASCII transliterations of Unicode text that recognize CJKV complex characters.


Usage
=====

You can run it on python3 interpreter:

.. code-block:: pycon

        from unihandecode import Unihandecoder
        d = Unihandecoder(lang='zh')
        print d.decode("\u660e\u5929\u660e\u5929\u7684\u98ce\u5439")
        # That prints: Ming Tian Ming Tian De Feng Chui 

        u = Unihandecoder(lang='ja')
        print d.decode('\u660e\u65e5\u306f\u660e\u65e5\u306e\u98a8\u304c\u5439\u304f')
        # That prints: Ashita ha Ashita no Kaze ga Fuku


Description
===========

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

This can be considered as an improved version of Python unidecode.
unidecode is Python port of Text::Unidecode Perl module by
Sean M. Burke <sburke@cpan.org>.

Requirements
============

It use a setuptools library to build and test.


Installation
============

You can install Unihandecode as usual

.. code-block:: pycon

        $ pip install unihandecode

Build
=====

You can build Unihandecode in recent way

.. code-block:: pycon

        $ python -m pep517.build ./

Test
====

You can run unit, lint, integration and regression tests with tox

.. code-block:: pycon

        $ tox


You can also run tests with launch pytest. To run pytest on project root,
please set PYTHONPATH to '<project_root>/src/'. It helps debugger to diagnose
problems.

.. code-block:: pycon

        $ pytest -vv

To launch lint test such as flake8;

.. code-block:: pycon

        $ tox -e check


SUPPORT
=======

 Questions, bug reports, useful code bits, and suggestions for
 Unihandecode are handled on `github project`_ page.

.. _`github project`: https://github.com/miurahr/unihandecode


AVAILABILITY
============

 The latest version of Unihandecode is available from
 Git repository in github.com:

        https://github.com/miurahr/unihandecode

 and Eggs are on PyPi.python.org:
 
        https://pypi.python.org/pypi/Unihandecode


COPYRIGHT
=========

Unicode Character Database:
 Date: 2010-09-23 09:29:58 UDT [JHJ]
 Unicode version: 6.0.0

 Copyright (c) 1991-2010 Unicode, Inc.
 For terms of use, see http://www.unicode.org/terms_of_use.html
 For documentation, see http://www.unicode.org/reports/tr44/

Unidecode's character transliteration tables:

Copyright 2001, Sean M. Burke <sburke@cpan.org>, all rights reserved.

Python code:

Copyright 2010-2014, Hiroshi Miura <miurahr@linux.com>
Copyright 2009, Tomaz Solc <tomaz@zemanta.com>


LICENSE
=======

Unihandecode
     Copyright 2010-2018,2020 Hiroshi Miura

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.


.. image:: https://d2weczhvl823v0.cloudfront.net/miurahr/unihandecode/trend.png
   :target: https://bitdeli.com/free
   :alt: Bitdeli

