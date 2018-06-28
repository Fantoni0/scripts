#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It concatenates previous sentences and current sentences in one line: prev BREAK curr
# It searches for the most similar sentence to prepend
# REQUIRES fasttext sent2vec (https://github.com/epfml/sent2vec)
# fantoni[o|0] (21/6/18)


# Similar to generateSimilarConcatenatedCorpus.py
# It does not enforce the requirement of preprending a previous sentence. It appends the most similar one (it can be ahead)

import argparse
import subprocess

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''

parser = argparse.ArgumentParser(description="Takes a route to the dataset files and preprends the most similar(past) sentence to each sentence", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Locations")
parser.add_argument('-n', '--sentences', type=int, help="Number of sentences to concatenate")
parser.add_argument('-s', '--source', type=str, help="Source language of the splits")
parser.add_argument('-t', '--target', type=str, help="Target languages of the split. Use the same order as in datasets")

# Get parameters
args = parser.parse_args()
dataset =  args.dataset
n = args.sentences
source = args.source
target = args.target

# Create Folder
folderName = 'similarFastConcatenated-%d' % n 
createFolder = ['mkdir','-p', '%s/%s' % (dataset, folderName)]
subprocess.call(createFolder, shell=False)
subprocess.call(['mkdir','-p', 'tmp'], shell=False) # Create tmp directory

# Concatenate sentences
for idx, s in enumerate(['training', 'dev']): # Do not apply concatenation to test set
    for l in [source, target]:
        f = open(dataset+'/'+s+'.'+l, 'r')
	fo = open(dataset+'/'+folderName+'/'+s+'.'+l, 'w')
        fl = f.readlines()
	fl = [line.strip() for line in fl] # Remove \n 
	nfl = n*['<pad>'] + fl
	# Train Model using sent2vec
        subprocess.call(['fasttext', 'sent2vec', '-input', '%s.%s' % (s,l), '-output', 'tmp/model_%s_%s' % (s,l), '-epoch', '10', '-lr', '0.2', '-wordNgrams', '5', '-loss', 'ns', '-neg', '10', '-thread', '20', '-t', '0.00005', '-dropoutK', '6', '-bucket', '6000000'], shell=False)

	# Get most similar sentences in an output file
        with open(dataset+'/'+s+'.'+l, 'r') as infile:
            with open(dataset+'/tmp/out.txt', 'w') as outfile:
                subprocess.call(['fasttext', 'nnSent', dataset+'/tmp/model_%s_%s.bin' % (s,l), '%s.%s' % (s,l) , '%d' % (n+1)],stdin=infile, stdout=outfile, shell=False)
     	
	# Get the n most similar sentences
        fo2 = open('tmp/out.txt','r')
        fl2 = fo2.readlines()[1:-1] # Remove first line, contains log information. Last line is a \n
	fl2 = [line.strip() for line in fl2 if line!='\n'] # Remove lines containing just \n and trim the other
	
	j = 0
	for i in range(len(fl)):
	    #if i%2 != 0: # We get odd lines. Since the first liine contains the sentence itself
	    fo.write(' BREAK '.join(fl2[j:j+n])+' BREAK '+''.join(fl[i])+'\n')
	    j = i + n
	#else:j = i
	fo.close()
        fo2.close()
# Remove tmp directory
subprocess.call(['rm','-rf', 'tmp'], shell=False)
