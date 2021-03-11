from safeway_funcs import safeway_get_store_information
import argparse
from tqdm import trange
from json import dump

parser = argparse.ArgumentParser(description="Queries server for Safeway store information")
args = parser.parse_args()
outlist = []

for storenumber in trange(10000):
	if store_info := safeway_get_store_information(storenumber):
		outlist.append(store_info)
		
with open(f'safeway_stores.txt', 'w') as outfile:
	dump(sorted(outlist, key = lambda i: i['number']), outfile, indent=2)
