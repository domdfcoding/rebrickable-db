# stdlib
import os
import posixpath
from urllib.parse import urlparse

# 3rd party
import requests
from domdf_python_tools.paths import PathPlus

output_dir = PathPlus("rebrickable_db/data")
output_dir.mkdir(exist_ok=True, parents=True)

for link in [
		"https://cdn.rebrickable.com/media/downloads/themes.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/colors.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/parts.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/elements.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/sets.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/inventories.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/inventory_sets.csv.gz",
		"https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz",
		]:
	resp = requests.get(link)
	resp.raise_for_status()
	parts = urlparse(link)
	output_file = output_dir / posixpath.split(parts.path)[-1]
	output_file.write_bytes(resp.content)

# Colour mapping data; requires API key

headers = {"Accept": "application/json", "Authorization": f"key {os.environ['REBRICKABLE_API_KEY']}"}

resp = requests.get("https://rebrickable.com/api/v3/lego/colors/", headers=headers)
resp.raise_for_status()
resp_json: dict = resp.json()
colours_json: list = resp_json["results"]

while resp_json.get("next"):
	resp = requests.get(resp_json["next"], headers=headers)
	resp.raise_for_status()
	resp_json = resp.json()
	colours_json.extend(resp_json["results"])

output_file = output_dir / "colours.json"
output_file.dump_json(colours_json, indent=2)
