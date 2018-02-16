#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It extracts N random lines from M files. Creating N*M set files
# fantoni[o|0] (4/7/17)

import argparse
import sys
import operator
import random

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes average length of sentences and words", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, nargs='+', help="Dataset Locations")
parser.add_argument('-n', '--lines', type=int, nargs='+', help="Number of lines to extract from each split")
parser.add_argument('-s', '--source', type=str, nargs='+', help="Source language of the splits")
parser.add_argument('-t', '--target', type=str, nargs='+', help="Target languages of the split. Use the sema order as in datasets")


'''
    Example of usage:
        python extractSplits.py -ds xerox/enfr xerox/enes xerox/ende -n 10000 300 250 -s en -t fr es de
   
    It will extract 10000 random lines from xerox/enfr/training.[en|fr], xerox/enes/training.[en|es] and xerox/ende/training.[en|de] and it will store them in ./training.[src|trg]
    It will extract 300 random lines from xerox/enfr/dev.[en|fr], xerox/enes/dev.[en|es] and xerox/ende/dev.[en|de] and it will store them in ./dev.[src|trg]
    It will extract 250 random lines from xerox/enfr/test.[en|fr], xerox/enes/test.[en|es] and xerox/ende/test.[en|de] and it will store them in ./test.[src|trg]
'''

#Short Mode only prints training set stats in one line

args = parser.parse_args()
datasets =  args.dataset
lines = args.lines
source = args.source[0]
target = args.target

for idx, s in enumerate(['training', 'dev', 'test']):
    source_lines = []    
    tar_lines = []
    for idx2, d in enumerate(datasets):
	faux = open(d+'/'+s+'.'+source, 'r')
	size_lines = len(faux.readlines())
	faux.close()
        rindexes = random.sample([i for i in xrange(size_lines)], lines[idx])
	for l in [source, target[idx2]]:                      
            f = open(d+'/'+s+'.'+l, 'r')
            fl = f.readlines()                
            fl = [fl[i] for i in rindexes]
            if l in source:
                source_lines = source_lines + fl
            else:
                tar_lines = tar_lines + fl
            f.close()
    fout1 = open(s+'.src','a')
    fout2 = open(s+'.trg','a')
    fout1.writelines(source_lines)
    fout2.writelines(tar_lines)
    fout1.close()
    fout2.close()
        

        


        
        
