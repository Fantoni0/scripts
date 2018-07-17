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
parser.add_argument('-s', '--save', action='store_true', default=False, help="Optional parameter to save previous sentences in a separated file")


# Get parameters
args = parser.parse_args()
path =  args.path
p = args.prev_sentences
save = args.save

# Get name and file extension
pathFile = path.split('/')[-1].split('.')
fileName = ''.join(pathFile[:-1])
fileExt = pathFile[-1]

# De-concatenate sentences
f = open(path, 'r')
fo = open('/'.join(path.split('/')[:-1])+fileName+'_deconcatenated.'+fileExt , 'w')
fl = f.readlines()
fl = [line.strip() for line in fl] # Remove \n
if save:
    fp = open('/'.join(path.split('/')[:-1])+fileName+'_previousSent.'+fileExt , 'w')

for i in range(len(fl)):
    split_s = fl[i].split(' BREAK ')
    special_case = i == 0 or i == len(fl) - 1

    if i == 0 and save: # If it is the first line do nothing. 
        print()
    elif i == len(fl) - 1 and save: #If it is the last line we need to save both sentences
        fp.write(split_s[p-1]+'\n')        
        fp.write(split_s[p]+'\n')                
    
    if len(split_s) == 1:
        if save and not special_case:
            fp.write(fl[i]+'\n')       
        fo.write(fl[i]+'\n')
    else:
        if save and not special_case:
            fp.write(split_s[p-1]+'\n')
        fo.write(split_s[p]+'\n')
f.close()
fo.close()
fp.close()      
