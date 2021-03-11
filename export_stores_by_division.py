from safeway_funcs import safeway_get_store_information
import argparse
from tqdm import trange
from json import load

parser = argparse.ArgumentParser(description="List stores by division")
args = parser.parse_args()


with open(f'safeway_stores.txt') as json_file: 
	stores = load(json_file)


divisions = []

for store in stores:
	if store.get('division').get('name') not in divisions:
		divisions.append(store.get('division').get('name'))

for division in divisions:
	with open(f'{division}_stores.txt', 'w') as outfile: 
		for store in stores:
			if store.get('division').get('name') == division:
				outfile.write(f"{store.get('number')} - {store.get('brand').get('name')} - {store.get('address').get('line1')} - {store.get('address').get('city')} - {store.get('address').get('state')}\n")

		