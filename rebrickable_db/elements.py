# stdlib
import csv
import functools
import gzip
import typing
from collections import defaultdict
from types import MappingProxyType
from typing import Dict, List, NamedTuple

# 3rd party
from domdf_python_tools.compat import importlib_resources

__all__ = ["Element", "load", "load_mapping_to"]


class Element(NamedTuple):
	element_id: int
	part_num: str  # Encodes printing
	color_id: int
	design_id: str  # Just the mould


@functools.lru_cache(1)
def load() -> List[Element]:

	annotations = typing.get_type_hints(Element)
	data = []

	with gzip.open(importlib_resources.files("rebrickable_db.data") / "elements.csv.gz", "rt") as f:
		reader = csv.DictReader(f)
		for row in reader:
			data.append(Element(**{k: annotations[k](v) for k, v in row.items()}))

	return data
