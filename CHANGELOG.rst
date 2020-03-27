====================
Unihandecode ChangeLog
====================

All notable changes to this project will be documented in this file.

Unreleased_
===========

Added
-----

Changed
-------

Fixed
-----

Deprecated
----------

Removed
-------

Security
--------


`v0.9a2`_ (26, May, 2020)
=========================

Changed
-------

* Bump dependency pykakasi to v2.0.0a5
* test: move to pytest
* Add composition tests


`v0.9a1`_ (18, May, 2020)
=========================

Changed
-------

* Refactoring module consolidated into __init__.py
* Do not compress pickle database.
* Upgrade build workflow and build system.
* Add github-actions workflows


`v0.81`_ (1, May, 2018)
=======================

Changed
-------

* Use six for Python2 compatibility in unit test.

Fixed
-------

* Add missing dependency in setup.py
* Twine upload password environment on AppVeyor.yml

Deprecated
----------

* Drop support for python 2.6 and before.
* Use unittest instead of unittest2.


`v0.80`_ (30, April, 2018)
==========================

Added
-----

* Experimental support for Cantonease
* Coverage instrumentation
* Instrument coverage on Coveralls.io.
* Notify gitter about release and test

Changed
-------

* Improve Python 2/3 compatibility in data
* Use Six for Python 2/3 compatibility
* Use unittest2 for Python2
* test python versions: 2.7, 3.5, 3.6

Fixed
-----

* Clean up build process
* Loading Itaiji dictionary correctly.

Removed
-------

* Drop bundled PyKakasi and refers as dependency


`v0.50`_ (25, April, 2015)
==========================

* fix some bugs
* Update dictionary

`v0.45`_ (26, September, 2014)
==============================

* compress codepoints
* nose and tox test

`v0.43`_ (13, October, 2013)
============================

* pickle unicode_point

`v0.42`_ (7, October, 2013)
===========================

* work in progress

.. _Unreleased: https://github.com/miurahr/unihandecode/compare/v0.9a1...HEAD
.. _v0.9a1: https://github.com/miurahr/unihandecode/compare/v0.81...v0.9a1
.. _v0.81: https://github.com/miurahr/unihandecode/compare/v0.80...v0.81
.. _v0.80: https://github.com/miurahr/unihandecode/compare/v0.50...v0.80
.. _v0.50: https://github.com/miurahr/unihandecode/compare/v0.45...v0.50
.. _v0.45: https://github.com/miurahr/unihandecode/compare/v0.43...v0.45
.. _v0.43: https://github.com/miurahr/unihandecode/compare/v0.42...v0.43
.. _v0.42: https://github.com/miurahr/unihandecode/compare/v0.40...v0.42
