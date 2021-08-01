# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, help='directory where files are located')
args = parser.parse_args()

# definitions
filepath = args.filepath
outfile = os.path.join(filepath, 'avg_by_cat.csv')
os_filepath = os.fsencode(filepath)

cat_dict = {}
avg_dict = {}

for file in os.listdir(os_filepath):
	filename = os.fsdecode(file)
	if filename.endswith(".tsv"):
		with open(os.path.join(filepath, filename), 'r') as f:
			reader = csv.reader(f, delimiter = ' ')
			for row in reader:
				if len(row) != 2:
					continue
				cat = (row[0].split(':'))[0]
				if cat not in cat_dict:
					cat_dict[cat] = [int(row[1])/2]
				else:
					cat_dict[cat].append(int(row[1])/2)
	else:
		continue

for i in cat_dict:
	avg_dict[i] = sum(cat_dict[i])/len(cat_dict[i])

with open(outfile, 'w+') as g:
	writer = csv.writer(g, delimiter = '\t')
	for i in avg_dict:
		writer.writerow([i, avg_dict[i]])