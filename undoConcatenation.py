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
parser.add_argument('-pt', '--path', type=str, help="File Locations")

# Get parameters
args = parser.parse_args()
path =  args.path

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
    fo.write(fl[i].split(' BREAK ')[-1]+'\n')
f.close()
fo.close()
      
