#!/usr/bin/env python3
#
#  bind_requirements.py
"""
Bind requirements in ``requirements.txt`` files to the latest version on PyPI.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on https://github.com/pre-commit/pre-commit-hooks
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import sys
from typing import Iterable

# 3rd party
import click
import requests
from consolekit import click_command
from consolekit.options import auto_default_option
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from packaging.requirements import InvalidRequirement
from shippinglabel import normalize_keep_dot
from shippinglabel_pypi import bind_requirements
from urllib3.exceptions import MaxRetryError, NewConnectionError

# this package
from pre_commit_hooks.util import PASS

__all__ = ("main", )


@auto_default_option(
		"--specifier",
		type=click.STRING,
		help="The version specifier symbol to use. (default: %(default)s)",
		)
@click.argument("filenames", nargs=-1, type=click.STRING)
@click_command()
def main(filenames: Iterable[PathLike], specifier: str = ">=") -> None:
	"""
	Bind unbound requirements to the latest version on PyPI, and any later versions.
	"""

	retv = PASS

	for filename in filenames:
		filename = PathPlus(filename)
		try:
			ret_for_file = bind_requirements(filename, specifier, normalize_func=normalize_keep_dot)

			if ret_for_file:
				print(f"Binding requirements for {filename.as_posix()}")

		except (NewConnectionError, MaxRetryError, requests.exceptions.ConnectionError) as e:
			print(f"Error binding requirements for {filename.as_posix()}: {str(e)}")
			ret_for_file = 1
		except InvalidRequirement as e:
			print(f"Invalid Requirement: {str(e)}")
			ret_for_file = 1

		retv |= ret_for_file

	if not retv:
		print("Up to date.")

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())
