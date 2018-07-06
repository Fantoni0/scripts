#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It de-concatenates the specified file. Eg: prev BREAK curr --> curr
# fantoni[o|0] (20/6/18)

import argparse
import sys

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes average length of sentences and words", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-f', '--path', type=str, help="File Locations")
parser.add_argument('-p', '--prev_sentences', type=int, help="Number of previous senteces concatenated")

# Get parameters
args = parser.parse_args()
path =  args.path
p = args.prev_sentences

# Get name and file extension
pathFile = path.split('/')[-1].split('.')
fileName = ''.join(pathFile[:-1])
fileExt = pathFile[-1]

# De-concatenate sentences
f = open(path, 'r')
fo = open('/'.join(path.split('/')[:-1])+fileName+'_deconcatenated.'+fileExt , 'w')

fl = f.readlines()
fl = [line.strip() for line in fl] # Remove \n
for i in range(len(fl)):
    split_s = fl[i].split(' BREAK ')
    if len(split_s) == 1:
	fo.write(fl[i]+'\n')
    else:
        fo.write(split_s[p]+'\n')
f.close()
fo.close()
      
