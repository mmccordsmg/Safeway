from safeway_funcs import safeway_get_store_information
import argparse
from tqdm import trange
from json import load

with open(f'safeway_stores.txt') as json_file: 
	stores = load(json_file)

divisions = []
brands = []

for store in stores:
	if store.get('division').get('name') not in divisions:
		divisions.append(store.get('division').get('name'))
	if store.get('brand').get('name') not in brands:
		brands.append(store.get('brand').get('name'))

print(f'Divisions: {divisions}')
print(f'Brands: {brands}')
