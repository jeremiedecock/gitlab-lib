.. currentmodule:: TODO_PYTHON_PACKAGE_NAME

=================
Developer's notes
=================

Source code
~~~~~~~~~~~

The source code is currently `available on GitHub`_ under the terms and
conditions of the `MIT license`_. Fork away!


Getting Started For Developers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   the following guide is used only if you want to *develop* the
   `TODO_PYTHON_PACKAGE_NAME` package. If you just want to write code that uses it
   externally, you should rather install it as explained
   :ref:`there <introduction_section>`.

This guide assumes you are using the *Anaconda* Python distribution,
installed locally (*miniconda* should also work).

.. The following guidline is mostly taken from https://cta-observatory.github.io/ctapipe/_sources/getting_started/index.rst.txt

Step 1: Set up your package environment
+++++++++++++++++++++++++++++++++++++++

.. TODO: make a short introduction to explain what is a virtual environment and why it is recommanded to use it

.. TODO: explain the same things with the native venv alternative

In your terminal, change to the directory where you cloned `TODO_PYTHON_PACKAGE_NAME`, and type::

    conda env create -f environment.yml

This will create a conda virtual environment called `TODO_PYTHON_PACKAGE_NAME-dev` with all
the TODO_PROJECT_NAME dependencies and a few useful packages for development and
interaction.

If you want to give a different name to this environment, replace the previous
command by::

    conda env create -n NAME_OF_THE_ENVIROMENT -f environment.yml

and don't forget to adapt the following commands.

You can check the virtual environment has been successfully
created with the following command::

    conda env list

Next, switch to this new virtual environment:

* On Windows, in your Anaconda Prompt, run ``activate TODO_PYTHON_PACKAGE_NAME-dev``
* On MacOSX and Linux, in your Terminal, run ``source activate TODO_PYTHON_PACKAGE_NAME-dev``

You will need to type that last command any time you open a new
terminal to activate the virtual environment (you can of course
install everything into the base Anaconda environment without creating
a virtual environment, but then you may have trouble if you want to
install other packages with different requirements on the
dependencies).

If you want to see the list of packages installed in the virtual environment,
type::

    conda list -n TODO_PYTHON_PACKAGE_NAME-dev

If later you want to leave the `TODO_PYTHON_PACKAGE_NAME-dev` virtual environment:

* On Windows, in your Anaconda Prompt, run ``deactivate``
* On MacOSX and Linux, in your Terminal, run ``source deactivate``

Also if you want to completely remove this environment from your system, you
can type::

    conda remove --name TODO_PYTHON_PACKAGE_NAME-dev --all

See https://conda.io/docs/user-guide/tasks/manage-environments.html for more
information on Anaconda virtual environments.

Step 2: Setup TODO_PROJECT_NAME for development
+++++++++++++++++++++++++++++++++++

Now setup this cloned version for development. The following command
will make symlinks in your python library directory to your TODO_PROJECT_NAME
installation (it creates a `.pth` file, there is no need to set
PYTHONPATH, in fact it should be blank to avoid other problems). From
then on, all the TODO_PROJECT_NAME binaries and the library itself will be
usable from anywhere.

For Linux/MacOSX users, type::

    python3 setup.py develop

or as a shorter alternative::

    make develop

For Windows users, type::

    py setup.py develop

If you want to remove the

Bug reports
~~~~~~~~~~~

To search for bugs or report them, please use the Bug Tracker at:

    TODO_PROJECT_ISSUE_TRACKER_URL

Contribute
~~~~~~~~~~

This project is written for Python 3.x.
Python 2.x is *not* supported.

The `TODO.md`_ file contains the TODO list.

All contributions should at least comply with the following PEPs_:

- PEP8_ "Python's good practices"
- PEP257_ "Docstring Conventions"
- PEP287_ "reStructuredText Docstring Format"

All contribution should be properly documented and tested with unittest_
and/or doctest_.

pylint_, `pep8 <https://github.com/PyCQA/pep8>`__ and pyflakes_ should also be
used to check the quality of each module.

Docstrings should be compatible with the
`Sphinx "napoleon" extension <http://sphinxcontrib-napoleon.readthedocs.org/>`__
and follow the Numpy style:

- `Please follow this guide <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`__
- `Be inspired by these examples <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__

Changes
~~~~~~~

.. include:: ../CHANGES.rst
   :start-line: 2

.. ......................................................................... ..

.. _MIT license: https://opensource.org/licenses/MIT
.. _available on GitHub: TODO_PROJECT_GITHUB_URL
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _PEP257: https://www.python.org/dev/peps/pep-0257/
.. _PEP287: https://www.python.org/dev/peps/pep-0287/
.. _PEPs: https://www.python.org/dev/peps/
.. _unittest: https://docs.python.org/3/library/unittest.html
.. _doctest: https://docs.python.org/3/library/doctest.html
.. _pylint: http://www.pylint.org/
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _TODO.md: TODO_PROJECT_GITHUB_URL/blob/master/TODO.md
