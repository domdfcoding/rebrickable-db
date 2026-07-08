from pathlib import Path
import posixpath
from urllib.parse import urlparse
import requests

output_dir = Path("rebrickable_db/data")
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