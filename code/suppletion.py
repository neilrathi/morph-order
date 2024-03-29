# python suppletion.py --filedir ../../morph-sens/features/finnish_nouns_adj/results/forWords_Finnish_OptimizeOrder_Nouns_Coarse_FineSurprisal/ --filepath ../three_feats/ --pos NOUN --feat1 Number --feat2 Case

# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random, collections
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filedir', type=str, help='directory where files are located', required=True)
parser.add_argument('--filepath', type=str, help='output file path', required=True)
parser.add_argument('--pos', type=str, help='part of speech', required=True)
parser.add_argument('--feat1', type=str, help='first feature', required=True)
parser.add_argument('--feat2', type=str, help='second feature', required=True)
args = parser.parse_args()

# definitions
directory = args.filedir
filepath = args.filepath
pos = args.pos
feat1 = args.feat1
feat2 = args.feat2

def threefeat(pos, feat1, feat2):
	os_filepath = os.fsencode(filepath)

	final_dict = {}
	min_auc = {}
	feat1_pos = -1
	feat2_pos = -1

	auc = 1000000

	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
		if os.path.isfile(f):
			if (filename.endswith(".tsv")) and ((filename.split('_'))[-2] == pos):
				lang = ((filename.split('_'))[-4].split('-'))[0]
				if lang not in min_auc:
					min_auc[lang] = 10000000
				with open(os.path.join(directory, filename), 'r') as f:
					reader = csv.reader(f, delimiter = ' ')
					for row in reader:
						if len(row) != 2:
							if float(row[1]) < min_auc[lang]:
								auc = float(row[1])
							break
					if auc < min_auc[lang]:
						min_auc[lang] = auc
					else:
						continue
					for row in reader:
						if len(row) == 2:
							if row[0] == feat1:
								feat1_pos = int(row[1])/2
							if row[0] == feat2:
								feat2_pos = int(row[1])/2
					if feat1_pos >= 0 and feat2_pos >= 0:
						final_dict[lang] = feat1_pos - feat2_pos
		feat1_pos = -1
		feat2_pos = -1
		
	return final_dict

print(threefeat(pos, feat1, feat2))