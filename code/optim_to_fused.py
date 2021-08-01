# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, help='directory where files are located')
parser.add_argument('--optim', type=str, help='optimized ordering file')
parser.add_argument('--pmi', type=str, help='optimized ordering file')
parser.add_argument('--surps', type=str, help='surprisal file')
args = parser.parse_args()

# definitions
filepath = args.filepath
optim_name = args.optim
pmi_name = args.pmi
surps_name = args.surps

optim_file = os.path.join(filepath, optim_name)
opt_mi_file = os.path.join(filepath, pmi_name)
surps_file = os.path.join(filepath, surps_name)
rank_file = os.path.join(filepath, 'rank_diff.csv')
pmi_file = os.path.join(filepath, 'pmi_diff.csv')
udum_file = os.path.join(filepath, 'UD_UM.txt')

optim = pd.read_csv(optim_file, names = ['feats', 'tworank'], sep = '\t')
pmi = pd.read_csv(opt_mi_file, names = ['feat1', 'feat2', 'count', 'pmi'], sep = '\t')
surps = pd.read_csv(surps_file, names = ['feats', 'meansurp', 'medsurp', 'sdsurp'], sep = '\t')

udum_old = pd.read_csv(udum_file, header = None, index_col = 0, squeeze = True, sep = '\t').to_dict()
udum = dict((v, k) for k, v in udum_old.items())

tot_ranks = {}
tot_pmis = {}
feats_seen = []

for i, row in surps.iterrows():
	rank = []
	udfeats = []
	rowfeats = row['feats'].split(';')
	if set(rowfeats) in feats_seen:
		continue
	feats_seen.append(set(rowfeats))
	for i in range(1, len(rowfeats)):
		if rowfeats[i] in udum:
			udfeats.append(udum[rowfeats[i]])
	for j, row2 in optim.iterrows():
		if row2['feats'] in rowfeats:
			rank.append(row2['tworank']/2)
			rowfeats.remove(row2['feats'])
	for k, row3 in pmi.iterrows():
		if set([row3['feat1'], row3['feat2']]) == set(udfeats):
			cur_pmi = row3['pmi']
	if len(rank) != 2:
		print(rowfeats)
		continue
	rank_diff = abs(rank[0] - rank[1])
	if row['feats'] not in tot_ranks:
		tot_ranks[row['feats']] = rank_diff
	if row['feats'] not in tot_pmis:
		tot_pmis[row['feats']] = cur_pmi

with open(rank_file, 'w+') as f:
	writer = csv.writer(f, delimiter = '\t')
	for key, value in tot_ranks.items():
		writer.writerow([key, value])

with open(pmi_file, 'w+') as f:
	writer = csv.writer(f, delimiter = '\t')
	for key, value in tot_pmis.items():
		writer.writerow([key, value])