# python two_feat_compare.py  --filedir ../../morph-sens/features/finnish_nouns_adj/results/forWords_Finnish_OptimizeOrder_Nouns_Coarse_FineSurprisal/ --filepath ../

# Determines length-normalized standard deviation for all two-feature pairs
# based on optimized ordering from the ETH, across all possible languages.
# Minimum number of datapoints to be reported  = 7.

# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random, collections
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filedir', type=str, help='directory where files are located', required=True)
parser.add_argument('--filepath', type=str, help='output file path', required=True)
#parser.add_argument('-l', '--feats', help='delimited list input (comma separated, no spaces)', type=str)
args = parser.parse_args()

# definitions
directory = args.filedir
filepath = args.filepath
#feats_arg = [str(item) for item in args.feats.split(',')]

feats_list_set = set()
feat_dict = {}

def getfeats(lang):
	lang_feats_list = set()

	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
		if (os.path.isfile(f)) and (lang in filename):
			if (filename.endswith(".tsv")) and ((filename.split('_'))[-2] == 'VERB'):
				with open(os.path.join(directory, filename), 'r') as f:
					reader = csv.reader(f, delimiter = ' ')
					for row in reader:
						if len(row) == 2:
							cat = row[0]
							lang_feats_list.add(cat)

	return lang_feats_list

def lang_feats(lang):
	cat_dict = {}

	min_auc = 1000000000
	auc = 1000000

	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
		if (os.path.isfile(f)) and (lang in filename):
			if (filename.endswith(".tsv")) and ((filename.split('_'))[-2] == 'VERB'):
				with open(os.path.join(directory, filename), 'r') as f:
					reader = csv.reader(f, delimiter = ' ')
					for row in reader:
						if len(row) != 2:
							if float(row[1]) < min_auc:
								auc = float(row[1])
							break
					if auc < min_auc:
						min_auc = auc
						cat_dict.clear()
					else:
						continue
					for row in reader:
						if len(row) == 2:
							cat = row[0]
							if cat not in cat_dict:
								cat_dict[cat] = int(row[1])/2

	return cat_dict

lang_list = []

for filename in os.listdir(directory):
	if ((filename.split('_'))[7].split('-'))[0] not in lang_list:
		lang_list.append(((filename.split('_'))[7].split('-'))[0])

lang_dict = {}

for L in lang_list:
	lang_dict[L] = lang_feats(L)

for lang in lang_list:
	lang_feats_list = getfeats(lang)
	feats_list_set = feats_list_set.union(lang_feats_list)

feats_list = list(feats_list_set)

combos = itertools.combinations(feats_list, 2)
combo_dict = {}

for C in list(combos):
	for L in lang_list:
		skip_pass = False
		for f in list(C):
			if f not in lang_dict[L]:
				skip_pass = True
				break
		if skip_pass:
			continue
		f_pos = []
		for f in list(C):
			f_pos.append((lang_dict[L])[f])
		if set(C) == {'Case', 'Number'} or set(C) == {'Person', 'Number'}:
			print(L, C)
		if ''.join(list(C)) not in combo_dict:
			combo_dict[''.join(list(C))] = [(max(f_pos)-min(f_pos))/len(lang_dict[L])]
		else:
			combo_dict[''.join(list(C))].append((max(f_pos)-min(f_pos))/len(lang_dict[L]))

#outfile = os.path.join(filepath, f'twofeatdata.csv')

#with open(outfile, 'w+') as f:
#	writer = csv.writer(f, delimiter = '\t')
#	writer.writerow(['FeatureCombination', 'NormalizedSD'])
#	for i in combo_dict:
#		if len(combo_dict[i]) > 7:
#			writer.writerow([i, sum(combo_dict[i])/len(combo_dict[i])])
#		if i == "PersonNumber" or i == "NumberCase":
#			print(i, len(combo_dict[i]))