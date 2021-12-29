# python three_feat.py --filedir ../../morph-sens/features/finnish_nouns_adj/results/optimize_finegrained/ --filepath ../three_feats/ --feats Person,Number,Gender

# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random, collections
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filedir', type=str, help='directory where files are located', required=True)
parser.add_argument('--filepath', type=str, help='output file path', required=True)
parser.add_argument('-l', '--feats', help='delimited list input', type=str)
args = parser.parse_args()

# definitions
directory = args.filedir
filepath = args.filepath
feats_arg = [str(item) for item in args.feats.split(',')]

feat_dict = {}

def threefeat(lang):
	outfile = os.path.join(filepath, f'three_feat_{lang}.csv')
	os_filepath = os.fsencode(filepath)

	cat_dict = {}
	avg_dict = {}
	final_dict = {}
	out_dict = {}

	min_auc = 1000000000
	auc = 1000000

	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
		if (os.path.isfile(f)) and (lang in filename):
			if (filename.endswith(".tsv")) and (filename[-13] == 'B'):
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
							cat = (row[0].split(':'))[0]
							if cat not in cat_dict:
								cat_dict[cat] = [int(row[1])/2]
							else:
								cat_dict[cat].append(int(row[1])/2)

	for i in cat_dict:
		avg_dict[i] = sum(cat_dict[i])/len(cat_dict[i])

	avg_list = [k for k in sorted(avg_dict, key=avg_dict.get)]

	for i, j in enumerate(avg_list):
		final_dict[j] = i

	for x in itertools.combinations(avg_list, 3):
		feats = list(x)
		feat_rank_list = [final_dict[i] for i in feats]
		out_dict[','.join(feats)] = statistics.stdev(feat_rank_list)
		if collections.Counter(feats) == collections.Counter(feats_arg):
			feat_dict[lang] = statistics.stdev(feat_rank_list)/len(feat_rank_list)

	print(lang, feat_rank_list)

	with open(outfile, 'w+') as g:
		writer = csv.writer(g, delimiter = '\t')
		for i in out_dict:
			writer.writerow([i, out_dict[i]])

lang_list = []

for filename in os.listdir(directory):
	if ((filename.split('_'))[3].split('-'))[0] not in lang_list:
		lang_list.append(((filename.split('_'))[3].split('-'))[0])

for lang in lang_list:
	threefeat(lang)

print(feat_dict)