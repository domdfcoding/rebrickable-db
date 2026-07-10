#!/usr/bin/env python3
#
#  part_relationships.py
"""
Data on part relationships.
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
import functools
import typing
from typing import List, NamedTuple

# this package
from rebrickable_db.utils import gzip_csv_reader

__all__ = ["PartRelationship", "load"]


class PartRelationship(NamedTuple):
	"""
	Represents a relationship between one part and another part.
	"""

	rel_type: str  # TODO: enum
	child_part_num: str
	parent_part_num: str


@functools.lru_cache(1)
def load() -> List[PartRelationship]:
	"""
	Load the list of part relationships.
	"""

	annotations = typing.get_type_hints(PartRelationship)
	print(annotations)
	data = []

	with gzip_csv_reader("part_relationships.csv.gz") as reader:
		for row in reader:
			data.append(PartRelationship(**{k: annotations[k](v) for k, v in row.items()}))

	return data
