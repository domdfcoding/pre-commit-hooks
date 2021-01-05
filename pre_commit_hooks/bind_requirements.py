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
import argparse
import sys
from typing import Optional, Sequence

# 3rd party
import requests
from shippinglabel.pypi import bind_requirements
from urllib3.exceptions import MaxRetryError, NewConnectionError  # type: ignore

# this package
from pre_commit_hooks.util import PASS

__all__ = ["main"]


def main(argv: Optional[Sequence[str]] = None) -> int:  # noqa: D103
	parser = argparse.ArgumentParser(
			description="Bind unbound requirements to the latest version on PyPI, and any later versions.",
			)
	parser.add_argument("filenames", nargs='*', help="Filenames to bind requirements for.")
	parser.add_argument(
			"--specifier",
			type=str,
			default=">=",
			help="The version specifier symbol to use. (default: %(default)s)",
			)

	args = parser.parse_args(argv)
	retv = PASS

	for filename in args.filenames:
		try:
			ret_for_file = bind_requirements(filename, args.specifier)

			if ret_for_file:
				print(f"Binding requirements for {filename}")

		except (NewConnectionError, MaxRetryError, requests.exceptions.ConnectionError) as e:
			print(f"Error binding requirements for {filename}: {str(e)}")
			ret_for_file = 1

		retv |= ret_for_file

	if not retv:
		print("Up to date.")

	return retv


if __name__ == "__main__":
	sys.exit(main())
