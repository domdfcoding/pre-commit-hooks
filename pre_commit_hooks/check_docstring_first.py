#!/usr/bin/env python3
#
#  check_docstring_first.py
"""
Checks the docstring does not occur after any code.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on https://github.com/pre-commit/pre-commit-hooks
#  Copyright (c) 2014 pre-commit dev team: Anthony Sottile, Ken Struys
#
#  Modified to permit multiple "docstring" like objects
#  as long as the first one is at the top of the file.
#  This is useful when writing Sphinx docstrings for attributes, variables etc.
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
import io
import tokenize
from tokenize import tokenize as tokenize_tokenize
from typing import Optional, Sequence

# this package
from pre_commit_hooks.util import FAIL, PASS

__all__ = ["check_docstring_first", "main"]

NON_CODE_TOKENS = frozenset((
		tokenize.COMMENT,
		tokenize.ENDMARKER,
		tokenize.NEWLINE,
		tokenize.NL,
		tokenize.ENCODING,
		))


def check_docstring_first(src: bytes, filename: str = "<unknown>") -> int:
	"""
	Returns nonzero if the source has what looks like a docstring that is
	not at the beginning of the source.

	A string will be considered a docstring if it is a STRING token with a
	col offset of 0.
	"""  # noqa: D400

	found_docstring_line = None
	found_code_line = None

	tok_gen = tokenize_tokenize(io.BytesIO(src).readline)

	for tok_type, _, (sline, scol), _, _ in tok_gen:
		# Looks like a docstring!
		if tok_type == tokenize.STRING and scol == 0:
			if found_docstring_line is not None:
				pass
			elif found_code_line is not None:
				print(
						f'{filename}:{sline} Module docstring appears after code '
						f'(code seen on line {found_code_line}).',
						)
				return FAIL
			else:
				found_docstring_line = sline
		elif tok_type not in NON_CODE_TOKENS and found_code_line is None:
			found_code_line = sline

	return PASS


def main(argv: Optional[Sequence[str]] = None) -> int:  # noqa: D103
	parser = argparse.ArgumentParser()
	parser.add_argument("filenames", nargs='*')
	args = parser.parse_args(argv)

	retv = PASS

	for filename in args.filenames:
		with open(filename, "rb") as f:
			contents = f.read()
		retv |= check_docstring_first(contents, filename=filename)

	return retv
