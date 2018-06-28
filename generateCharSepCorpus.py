#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It tokenizes the text, following each word we have its separated characters. E.g: Hello Tom --> Hello H e l l o Tom T o m
# fantoni[o|0] (25/6/18)

import argparse
import subprocess
from keras_wrapper import dataset as ds

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''

parser = argparse.ArgumentParser(description="Takes a route to the dataset files and preprends the most similar(past) sentence to each sentence", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Locations")
parser.add_argument('-s', '--source', type=str, help="Source language.")
parser.add_argument('-t', '--target', type=str, help="Target languages.")

# Get parameters
args = parser.parse_args()
dataset =  args.dataset
source = args.source
target = args.target

# Create Folder
folderName = 'separatedChar'
subprocess.call(['mkdir','-p', '%s' % folderName], shell=False) # Create directory

# Concatenate sentences
for idx, s in enumerate(['training', 'dev', 'test']):
    for l in [source, target]:
	if s != 'training' and l == target: # Do not apply to dev and test sets of target language
	   continue
        f = open(dataset+'/'+s+'.'+l, 'r')
	fo = open(dataset+'/'+folderName+'/'+s+'.'+l, 'w')
        fl = f.readlines()
	fl = [line.strip() for line in fl] # Remove \n
	for line in fl:
	    for idx, word in enumerate(line.split()):
		word = unicode(word, 'utf-8')
		w_tok = ds.tokenize_none_char(word)
		if idx + 1 == len(line.split()):
		    fo.write('<w> '+word.encode('utf-8') + ' ' + w_tok.encode('utf-8') + '\n')
		else:
		    fo.write('<w> '+word.encode('utf-8') + ' ' + w_tok.encode('utf-8') + ' ')
    f.close()
    fo.close()
