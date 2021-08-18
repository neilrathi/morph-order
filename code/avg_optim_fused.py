# basic imports
import re, os, io, time, csv, statistics, argparse, itertools, random
import operator
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, help='directory where files are located')
parser.add_argument('--udum', type=str, help='UD-UM helper file')
parser.add_argument('--optim', type=str, help='optimized orderings file (UD)')
parser.add_argument('--surps', type=str, help='unimorph fusion file')
args = parser.parse_args()

# definitions
filepath = args.filepath
optim_name = args.optim
udum_name = args.udum
surps_name = args.surps

optim_file = os.path.join(filepath, optim_name)
udum_file = os.path.join(filepath, udum_name)
surps_file = os.path.join(filepath, surps_name)
rank_file = os.path.join(filepath, 'avg_rank_diff.csv')

optim = pd.read_csv(optim_file, names = ['feats', 'tworank'], sep = '\t')
optim[['cat', 'feat']] = optim['feats'].str.split(':', expand=True)

surps = pd.read_csv(surps_file, names = ['feats', 'meansurp', 'medsurp', 'sdsurp'], sep = '\t')
surps[['POS', 'f1', 'f2']] = surps['feats'].str.split(';', expand=True)

udum = pd.read_csv(udum_file, names = ['UD', 'UM'], sep = '\t')
udum['UD'] = udum['UD'].str.replace('=', ':')
udum[['cat','feat']] = udum['UD'].str.split(':', expand=True)

optim_dict_un = dict()
optim_avg_dict = dict()

for i, row in optim.iterrows():
	if optim.iloc[i]['cat'] in optim_avg_dict:
		optim_avg_dict[optim.iloc[i]['cat']].append(optim.iloc[i]['tworank']/2)
	else:
		optim_avg_dict[optim.iloc[i]['cat']] = [optim.iloc[i]['tworank']/2]

for k in optim_avg_dict:
	optim_dict_un[k] = statistics.mean(optim_avg_dict[k])

sorted_tuples = sorted(optim_dict_un.items(), key = operator.itemgetter(1))
optim_dict = {k: v for k, v in sorted_tuples}

for i, k in enumerate(optim_dict):
	optim_dict[k] = i

udum_dict = {v: k for k, v in zip(udum["cat"], udum["UM"])}
surps['c1'] = surps['f1'].map(udum_dict)
surps['c2'] = surps['f2'].map(udum_dict)
surps['p1'] = surps['c1'].map(optim_dict)
surps['p2'] = surps['c2'].map(optim_dict)

surps = surps.drop(columns = ['medsurp', 'sdsurp', 'POS', 'f1', 'f2'])

surps['rank'] = abs(surps['p1'] - surps['p2'])
print(surps.head())
surps.to_csv(rank_file, sep='\t')