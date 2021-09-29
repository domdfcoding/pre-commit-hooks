#################
pre-commit-hooks
#################

.. start short_desc

**Some useful hooks for pre-commit.**

.. end short_desc

Now with 2× as many hooks!

See also: https://github.com/pre-commit/pre-commit

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/pre-commit-hooks/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/pre-commit-hooks/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/domdfcoding/pre-commit-hooks/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/domdfcoding/pre-commit-hooks/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/pre-commit-hooks/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/pre-commit-hooks?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/pre-commit-hooks?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/pre-commit-hooks
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/domdfcoding/pre-commit-hooks
	:target: https://github.com/domdfcoding/pre-commit-hooks/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/pre-commit-hooks
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/pre-commit-hooks/v0.2.1
	:target: https://github.com/domdfcoding/pre-commit-hooks/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/pre-commit-hooks
	:target: https://github.com/domdfcoding/pre-commit-hooks/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. end shields

Using pre-commit-hooks with pre-commit
---------------------------------------

Add this to your ``.pre-commit-config.yaml``

.. code-block:: yaml

	-   repo: https://github.com/domdfcoding/pre-commit-hooks
	    rev: v0.2.1  # Use the ref you want to point at
	    hooks:
	    -   id: requirements-txt-sorter
	    # -   id: ...

Hooks available
-----------------

``requirements-txt-sorter``
Sorts `PEP 508 <https://www.python.org/dev/peps/pep-0508/>`_ entries in requirements.txt and removes invalid entries, including ``pkg-resources==0.2.1``.

``check-docstring-first``
Checks that the docstring occurs before any module code, but allows additional "docstrings", such as for documenting variables with Sphinx.
