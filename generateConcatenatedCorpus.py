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
parser.add_argument('-n', '--next_sentences', type=int, help="Number of future sentences to concatenate (next)")
parser.add_argument('-p', '--prev_sentences', type=int, help="Number of previous sentences to concatenate (previous)")
parser.add_argument('-s', '--source', type=str, help="Source language of the splits")
parser.add_argument('-t', '--target', type=str, help="Target languages of the split. Use the sema order as in datasets")

# Get parameters
args = parser.parse_args()
dataset =  args.dataset
p = args.prev_sentences
n = args.next_sentences
source = args.source
target = args.target

# Create Folder
folderName = 'concatenated-p%d-n%d' %  (p,n)
subprocess.call(['mkdir', '-p', '%s/%s' % (dataset, folderName) ], shell=False)

# Concatenate sentences
for idx, s in enumerate(['training', 'dev', 'test']): # We do not concatenate in the test set
    for l in [source, target]:                      
        f = open(dataset+'/'+s+'.'+l, 'r')
	fo = open(dataset+'/'+folderName+'/'+s+'.'+l, 'w')
        fl = f.readlines()
	fl = [line.strip() for line in fl] # Remove \n 
	pfl = p*['<pad>'] + fl
	nfl = fl[1:] + n*['<pad>']
        for i in range(len(fl)):
	    fo.write(' BREAK '.join(pfl[i:i+p])+' BREAK '+''.join(fl[i])+' BREAK '*(n>0)+ ' BREAK '.join(nfl[i:i+n]) +'\n')
    f.close()
    fo.close()
      
