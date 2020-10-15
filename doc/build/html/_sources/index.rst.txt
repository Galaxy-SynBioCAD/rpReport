rpReport's Documentation
========================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _rpBase: https://github.com/Galaxy-SynBioCAD/rpBase

Welcome to rpReport's documenation. This project parses rpSBML files to a single CSV report. The following information is returned:
   1. Global Score
   2. Rule Score
   3. dG:superscript:`'o`
   4. dG:superscript:`'m`
   5. dG Uncertainty
   6. FBA Flux results
   7. UniProt ID's
   8. Selenzyme scores

Note that if any of that information is missing, then nothing is returned in the CSV.

Usage
#####

First build the rpBase_ docker before building the local one:

.. code-block:: bash

   docker build -t brsynth/rpreport-standalone:v2 .

The docker can be called locally using the following command:

.. code-block:: bash

   python run.py -input input.tar -input_format tar -output output.csv

 
API
###

.. toctree::
   :maxdepth: 1
   :caption: Contents:

.. currentmodule:: rpTool

.. autoclass:: getInfo
    :show-inheritance:
    :members:
    :inherited-members:

.. autoclass:: writeLine
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: rpToolServe

.. autoclass:: runReport_hdd
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: run

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:
