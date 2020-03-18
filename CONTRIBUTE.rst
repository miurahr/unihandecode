==================
Contribution guide
==================

This is contribution guide for unihandecode project.
You are welcome to send a Pull-Request, reporting bugs and ask questions.

Resources
=========

- Project owner: Hiroshi Miura
- Bug Tracker:  Github issue `Tracker`_
- Status: beta
- Activity: low
- Code management: git
- Source: Github repository `Repository`_

.. _`Repository`: https://github.com/miurahr/unihandecode.git
.. _`Tracker`: https://github.com/miurahr/unihandecode/issues


Send patch
==========

Here is small amount rule when you want to send patch the project;

1. every proposal for modification should send as 'Pull Request'

1. each pull request can consist of multiple commits.

1. you are encourage to split modifications to individual commits that are logical subpart.

CI tests
=========

Unihandecode project configured to use Github Actions, AppVeyor, Travis-CI and Coveralls
for regression test. You can see test results on badge and see details in a web page linked from badge.
All pull-requests are checked with CI environment automatically.

Local test
==========

To run test, you can do it as ordinary::

    tox
