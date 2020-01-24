#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# Applies a detokenization function to a given file
# fantoni[o|0] (17/4/18)

import argparse
import sys
import operator
from keras_wrapper import dataset


parser = argparse.ArgumentParser(description="Takes a file and applies a set of detokenization function from dataset class", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-f', '--file', type=str, required=True, help="File to detokenize")
parser.add_argument('-d', '--detokf', nargs='+', required=True, help="Detokenization Functions. Order matters")

args = parser.parse_args()
fn =  args.file
df = args.detokf

# Read Lines
fin = open(fn,'r')
lines = fin.readlines()
fout = open('detokenized_'+fn, 'w')
# Write each line in the new file after applying the detok. function
for l in lines:
    for func in df:
        l = eval('dataset.'+func)(l)
    fout.write(l.encode('utf-8')+'\n')

# Close buffers
fin.close()
fout.close()
