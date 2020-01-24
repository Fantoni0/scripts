#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It concatenates previous sentences and current sentences in one line: prev BREAK curr
# fantoni[o|0] (19/6/18)

import argparse
import subprocess
import sys
import operator
import random

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes average length of sentences and words", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Locations")
parser.add_argument('-ns', '--next_sentences', type=int, help="Number of future sentences to concatenate (next). Source side")
parser.add_argument('-ps', '--prev_sentences', type=int, help="Number of previous sentences to concatenate (previous). Source side")
parser.add_argument('-nt', '--next_sentences2', type=int, help="Number of future sentences to concatenate (next). Target side")
parser.add_argument('-pt', '--prev_sentences2', type=int, help="Number of previous sentences to concatenate (previous). Target side")
parser.add_argument('-s', '--source', type=str, help="Source language of the splits")
parser.add_argument('-t', '--target', type=str, help="Target languages of the split. Use the sema order as in datasets")

# Get parameters
args = parser.parse_args()
dataset =  args.dataset
ps = args.prev_sentences
ns = args.next_sentences
pt = args.prev_sentences2
nt = args.next_sentences2
source = args.source
target = args.target

# Create Folder
folderName = 'concatenated-ps%d-ns%d-pt%d-nt%d' %  (ps, ns, pt, nt)
subprocess.call(['mkdir', '-p', '%s/%s' % (dataset, folderName) ], shell=False)

# Concatenate sentences
for idx, s in enumerate(['training', 'dev', 'test']): # We do not concatenate in the test set
    for l in [source, target]:
	if l == source:
	    n_prev = ps
	    n_next = ns
	else:
	    n_prev = pt
	    n_next = nt
        f = open(dataset+'/'+s+'.'+l, 'r')
	fo = open(dataset+'/'+folderName+'/'+s+'.'+l, 'w')
        fl = f.readlines()
	fl = [line.strip() for line in fl] # Remove \n 
	pfl = n_prev*['<pad>'] + fl
	nfl = fl[1:] + n_next*['<pad>']
        for i in range(len(fl)):
	    fo.write(' BREAK '.join(pfl[i:i+n_prev])+' BREAK '+''.join(fl[i])+' BREAK '*(n_next>0)+ ' BREAK '.join(nfl[i:i+n_next]) +'\n')
    f.close()
    fo.close()
      
