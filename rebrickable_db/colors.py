# stdlib
import csv
import functools
import gzip
import json
import typing
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict, List, NamedTuple

# 3rd party
from domdf_python_tools.compat import importlib_resources

if TYPE_CHECKING:
	_int_empty = int
else:

	def _int_empty(val: str) -> int:
		if not val:
			return -1

		return int(val)


__all__ = ["Color", "load", "load_colour_map"]


class Color(NamedTuple):
	id: int
	name: str
	rgb: str
	is_trans: bool
	num_parts: int
	num_sets: int
	y1: _int_empty
	y2: _int_empty


@functools.lru_cache(1)
def load() -> List[Color]:

	annotations = typing.get_type_hints(Color)
	print(annotations)
	data = []

	with gzip.open(importlib_resources.files("rebrickable_db.data") / "colors.csv.gz", "rt") as f:
		reader = csv.DictReader(f)
		for row in reader:
			data.append(Color(**{k: annotations[k](v) for k, v in row.items()}))

	return data

