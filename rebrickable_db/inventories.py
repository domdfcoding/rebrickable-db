#!/usr/bin/env python3
#
#  inventories.py
"""
List of LEGO sets and their inventories.
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
from types import MappingProxyType
from typing import TYPE_CHECKING, Mapping, NamedTuple, Sequence, Union

# 3rd party
from domdf_python_tools.utils import strtobool

# this package
from rebrickable_db.utils import gzip_csv_reader

if TYPE_CHECKING:
	bool_type = bool
else:
	bool_type = strtobool

__all__ = [
		"Inventory",
		"InventoryMinifig",
		"InventoryPart",
		"InventorySet",
		"load_minfigs_inventory",
		"load_parts_inventory",
		"load_sets",
		"load_sets_inventory",
		]


class Inventory(NamedTuple):
	"""
	A set.
	"""

	id: int
	version: int
	set_num: str


@functools.lru_cache(1)
def load() -> Mapping[str, Inventory]:
	"""
	Load the list of sets.
	"""

	annotations = typing.get_type_hints(Inventory)
	data = {}

	with gzip_csv_reader("inventories.csv.gz") as reader:
		for row in reader:
			the_set = Inventory(**{k: annotations[k](v) for k, v in row.items()})
			data[the_set.set_num] = the_set

	return MappingProxyType(data)


class InventoryPart(NamedTuple):
	"""
	A part in a set inventory.
	"""

	inventory_id: int
	part_num: str
	color_id: int
	quantity: int
	is_spare: bool_type
	img_url: str


@functools.lru_cache(1)
def load_parts_inventory() -> Sequence[InventoryPart]:
	"""
	Load the set inventory parts.
	"""

	annotations = typing.get_type_hints(InventoryPart)
	data = []

	with gzip_csv_reader("inventory_parts.csv.gz") as reader:
		for row in reader:
			data.append(InventoryPart(**{k: annotations[k](v) for k, v in row.items()}))

	return tuple(data)


class InventoryMinifig(NamedTuple):
	"""
	A minifigure in a set inventory.
	"""

	inventory_id: int
	fig_num: str
	quantity: int


@functools.lru_cache(1)
def load_minfigs_inventory() -> Sequence[InventoryMinifig]:
	"""
	Load the set inventory minifigures.
	"""

	annotations = typing.get_type_hints(InventoryMinifig)
	data = []

	with gzip_csv_reader("inventory_minifigs.csv.gz") as reader:
		for row in reader:
			data.append(InventoryMinifig(**{k: annotations[k](v) for k, v in row.items()}))

	return tuple(data)


class InventorySet(NamedTuple):
	"""
	A set in a bundle's inventory.
	"""

	inventory_id: int
	set_num: str
	quantity: int


@functools.lru_cache(1)
def load_sets_inventory() -> Sequence[InventorySet]:
	"""
	Load the list of sets found in bundles.
	"""

	annotations = typing.get_type_hints(InventorySet)
	data = []

	with gzip_csv_reader("inventory_sets.csv.gz") as reader:
		for row in reader:
			data.append(InventorySet(**{k: annotations[k](v) for k, v in row.items()}))

	return tuple(data)


InventoryItem = Union[InventoryPart, InventoryMinifig, InventorySet]
