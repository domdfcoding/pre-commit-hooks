#!/usr/bin/env python3
#
#  requirements_txt_sorter.py
"""
Sort requirements in ``requirements.txt`` files alphabetically.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on https://github.com/pre-commit/pre-commit-hooks
#  Copyright (c) 2014 pre-commit dev team: Anthony Sottile, Ken Struys
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
from typing import Iterable, List, Set

# 3rd party
import click
from consolekit import click_command
from consolekit.options import flag_option
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike
from shippinglabel import normalize_keep_dot
from shippinglabel.requirements import ComparableRequirement, read_requirements

# this package
from pre_commit_hooks.util import FAIL, PASS

__all__ = ("sort_requirements", "main")


def sort_requirements(filename: PathLike, allow_git: bool = False) -> int:
	"""
	Sort the requirements in the given file alphabetically.

	:param filename: The file to sort the requirements in.
	:param allow_git: Whether to allow lines that start with ``git+``, which are allowed by pip but not :pep:`508`.
	"""

	ret = PASS
	filename = PathPlus(filename)
	comments: List[str]
	requirements: Set[ComparableRequirement]
	git_lines: List[str] = []

	requirements, comments, invalid_lines = read_requirements(
		req_file=filename,
		include_invalid=True,
		normalize_func=normalize_keep_dot,
		)

	for line in invalid_lines:
		if line.startswith("git+") and allow_git:
			git_lines.append(line)
		else:
			ret |= FAIL

	# find and remove pkg-resources==0.0.0
	# which is automatically added by broken pip package under Debian
	if ComparableRequirement("pkg-resources==0.0.0") in requirements:
		requirements.remove(ComparableRequirement("pkg-resources==0.0.0"))
		ret |= FAIL

	sorted_requirements = sorted(requirements)

	buf = StringList([*comments, *git_lines, *[str(req) for req in sorted_requirements]])
	buf.blankline(ensure_single=True)

	if (requirements != sorted_requirements and buf != filename.read_lines()) or ret:
		print('\n'.join(buf))
		# print(coloured_diff(
		# 		filename.read_lines(),
		# 		buf,
		# 		str(filename),
		# 		str(filename),
		# 		"(original)",
		# 		"(sorted)",
		# 		lineterm='',
		# 		))
		ret |= FAIL
		filename.write_lines(buf)

	return ret


@flag_option(
		"--allow-git",
		default=False,
		help="allow 'git+' options, which are allowed by pip but not PEP 508.",
		)
@click.argument("filenames", nargs=-1, type=click.STRING)
@click_command()
def main(filenames: Iterable[str], allow_git: bool = False) -> None:  # noqa: PRM002
	"""
	Sort requirements in the given files.
	"""

	retv = PASS

	for arg in filenames:
		ret_for_file = sort_requirements(arg, allow_git=allow_git)

		if ret_for_file:
			print(f"Sorting {arg}")

		retv |= ret_for_file

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())
