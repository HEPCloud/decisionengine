.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Welcome to decisionengine's documentation!
==========================================

The Decision Engine is a critical component of the HEP Cloud Facility. It provides the
functionality of resource scheduling for disparate resource providers, including those
which may have a cost or restricted allocation of cycles.
This package, decisionengine, provides the framework and base classes, the
`decisionengine_modules </decisionengine_modules/>`_ package contains provider
specific implementations of the base classes.

Release Notes
=============

.. toctree::
   :maxdepth: 1

   release_notes
   Latest<release_notes/release_notes_2.0>


Install Decision Engine
=======================

Here are instructions for operators and developers to install the
Decision Engine using the distributed RPM packages.

.. toctree::
   :maxdepth: 1

   install
   install_el7
   install_el8


Developer Documentation
=======================

The developer documentation is in the `GitHub Wiki <https://github.com/HEPCloud/decisionengine/wiki/Development-Workflow>`_

Instructions to build the package, or to run unit tests and other CI tests, and to install decisionengine
are in the `GitHub Wiki <https://github.com/HEPCloud/decisionengine/wiki/How-to-Run-Decision-Engine>`_ as well.


Jenkins CI pipeline
===================

.. toctree::
   :maxdepth: 1

   jenkins.rst

Source code
===========

.. toctree::
   :maxdepth: 1

   Code documentation<code/index>
   code/decisionengine

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
