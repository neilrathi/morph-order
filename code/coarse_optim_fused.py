# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, help='directory where files are located')
parser.add_argument('--optim', type=str, help='optimized ordering file')
# parser.add_argument('--pmi', type=str, help='optimized ordering file')
parser.add_argument('--coarseoptim', type=str, help='optimized ordering file')
parser.add_argument('--surps', type=str, help='surprisal file')
args = parser.parse_args()

# definitions
filepath = args.filepath
optim_name = args.optim
# pmi_name = args.pmi
coarse_optim_name = args.coarseoptim
surps_name = args.surps

optim_file = os.path.join(filepath, optim_name)
optim_coarse_file = os.path.join(filepath, coarse_optim_name)
# opt_mi_file = os.path.join(filepath, pmi_name)
surps_file = os.path.join(filepath, surps_name)
rank_file = os.path.join(filepath, 'rank_diff.csv')
# pmi_file = os.path.join(filepath, 'pmi_diff.csv')
coarse_file = os.path.join(filepath, 'coarse_rank_diff.csv')
udum_file = os.path.join(filepath, 'UD_UM.txt')
umcat_file = os.path.join(filepath, 'UD_UM_sep.txt')

with open(umcat_file, 'r') as f:
	i = 0
	reader = csv.reader(f, delimiter=',')

optim = pd.read_csv(optim_file, names = ['feats', 'tworank'], sep = '\t')
optim_coarse = pd.read_csv(optim_coarse_file, names = ['feats', 'tworank'], sep = '\t')
# pmi = pd.read_csv(opt_mi_file, names = ['feat1', 'feat2', 'count', 'pmi'], sep = '\t')
surps = pd.read_csv(surps_file, names = ['feats', 'meansurp', 'medsurp', 'sdsurp'], sep = '\t')

udum_old = pd.read_csv(udum_file, header = None, index_col = 0, squeeze = True, sep = '\t').to_dict()
umcat_old = pd.read_csv(umcat_file, index_col = 0, squeeze = True, sep = ',')
udum = dict((v, k) for k, v in udum_old.items())
um_cat = umcat_old[['um', 'V1']].copy()
um_cat_dict = dict(um_cat.values)

tot_ranks = {}
# tot_pmis = {}
tot_coarse_ranks = {}
feats_seen = []

for i, row in surps.iterrows():
	rank = []
	udfeats = []
	cats = []
	coarse_rank = []
	rowfeats = row['feats'].split(';')
	if set(rowfeats) in feats_seen:
		continue
	feats_seen.append(set(rowfeats))
	for i in range(1, len(rowfeats)):
		if rowfeats[i] in udum:
			udfeats.append(udum[rowfeats[i]])
			cats.append(um_cat_dict[rowfeats[i]])
	for j, row2 in optim.iterrows():
		if row2['feats'] in rowfeats:
			rank.append(row2['tworank']/2)
			rowfeats.remove(row2['feats'])
	rowfeats = row['feats'].split(';')
	#for k, row3 in pmi.iterrows():
	#	if set([row3['feat1'], row3['feat2']]) == set(udfeats):
	#		cur_pmi = row3['pmi']
	for l, row4 in optim_coarse.iterrows():
		if row4['feats'] in cats:
			coarse_rank.append(row4['tworank']/2)
	if len(rank) != 2 or len(coarse_rank) != 2:
		print(rowfeats, rank)
		continue
	rank_diff = abs(rank[0] - rank[1])
	coarse_rank_diff = abs(coarse_rank[0] - coarse_rank[1])
	if row['feats'] not in tot_ranks:
		tot_ranks[row['feats']] = rank_diff
		cat_feats = ';'.join(cats)
		if cat_feats not in tot_coarse_ranks:
			tot_coarse_ranks[cat_feats] = [coarse_rank_diff, [row['meansurp']]]
		else:
			diff_surp = tot_coarse_ranks[cat_feats]
			diff = diff_surp[0]
			surp = diff_surp[1]
			surp.append(row['meansurp'])
			tot_coarse_ranks[cat_feats] = [diff, surp]
	#if row['feats'] not in tot_pmis:
	#	tot_pmis[row['feats']] = cur_pmi

with open(rank_file, 'w+') as f:
	passed_keys = []
	writer = csv.writer(f, delimiter = '\t')
	for key, value in tot_ranks.items():
		if set(key.split(';')) in passed_keys:
			continue
		passed_keys.append(set(key.split(';')))
		writer.writerow([key, value])

"""with open(pmi_file, 'w+') as f:
	passed_keys = []
	writer = csv.writer(f, delimiter = '\t')
	for key, value in tot_pmis.items():
		if set(key.split(';')) in passed_keys:
			continue
		passed_keys.append(set(key.split(';')))
		writer.writerow([key, value])"""

with open(coarse_file, 'w+') as f:
	passed_keys = []
	writer = csv.writer(f, delimiter = '\t')
	for key, value in tot_coarse_ranks.items():
		if set(key.split(';')) in passed_keys:
			continue
		passed_keys.append(set(key.split(';')))
		writer.writerow([key, value[0], sum(value[1])/len(value[1])])
