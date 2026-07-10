#!/usr/bin/env python3
#
#  utils.py
"""
General utilities.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import csv
import gzip
from contextlib import contextmanager
from typing import Iterator

# 3rd party
from domdf_python_tools.compat import importlib_resources

__all__ = ["gzip_csv_reader"]


@contextmanager
def gzip_csv_reader(filename: str) -> Iterator[csv.DictReader]:
	"""
	Read a gzipped CSV file.

	:param filename: The name of the resource in the package.
	"""

	with gzip.open(
			importlib_resources.files("rebrickable_db.data") / filename,
			"rt",
			) as f:  # type: ignore[call-overload]
		yield csv.DictReader(f)
