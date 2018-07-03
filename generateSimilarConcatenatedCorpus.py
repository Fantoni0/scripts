#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It concatenates previous sentences and current sentences in one line: prev BREAK curr
# It searches for the most similar sentence to prepend
# REQUIRES fasttext sent2vec (https://github.com/epfml/sent2vec)
# fantoni[o|0] (21/6/18)

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
folderName = 'similarConcatenated-%d' % n 
createFolder = ['mkdir','-p', '%s/%s' % (dataset, folderName)]
subprocess.call(createFolder, shell=False)
subprocess.call(['mkdir','-p', 'tmp'], shell=False) # Create tmp directory

# Concatenate sentences
for idx, s in enumerate(['training', 'dev', 'test']): # Do not apply concatenation to test set
    for l in [source, target]:
        f = open(dataset+'/'+s+'.'+l, 'r')
	fo = open(dataset+'/'+folderName+'/'+s+'.'+l, 'w')
        fl = f.readlines()
	fl = [line.strip() for line in fl] # Remove \n 
	nfl = n*['<pad>'] + fl
	# Train Model using sent2vec
        subprocess.call(['fasttext', 'sent2vec', '-input', '%s.%s' % (s,l), '-output', 'tmp/model_%s_%s' % (s,l), '-epoch', '10', '-lr', '0.2', '-wordNgrams', '5', '-loss', 'ns', '-neg', '10', '-thread', '20', '-t', '0.00005', '-dropoutK', '6', '-bucket', '6000000'], shell=False)
        for i in range(len(fl)):
	    if i > n+1:
		# Load previous sentences in a file. use a 30 
		with open(dataset+'/tmp/corpora.txt', 'w') as outfile:
		    subprocess.call(['sed', '-n', '%d,%dp;%dq' % (max(1, i-30),i-1 ,i),  '%s.%s' % (s,l)], stdout=outfile, shell=False)

		# Load sentence to query for most similar sentences
		with open(dataset+'/tmp/query.txt', 'w') as outfile:
		    subprocess.call(['sed', '%dq;d' % i, '%s.%s' % (s,l)], stdout=outfile, shell=False)
		
		# Get most similar sentences in an output file
		with open( dataset+'/tmp/query.txt', 'r') as infile:
		    with open(dataset+'/tmp/out.txt', 'w') as outfile:
			subprocess.call(['fasttext', 'nnSent', dataset+'/tmp/model_%s_%s.bin' % (s,l), dataset+'/tmp/corpora.txt', '%d' % (n+1)],stdin=infile, stdout=outfile, shell=False)

		# Get the n most similar sentences
		fo2 = open('tmp/out.txt','r')
		fl2 = fo2.readlines()[2:-1] # Remove first line, contains log information. The second one contains the sentence itself. Last line is a \n
		fl2 = [' '.join(line.strip().split()[2:]) for line in fl2]
		fo.write(' BREAK '.join(fl2)+' BREAK '+''.join(fl[i])+'\n')		
		fo2.close()
	    else: # For N first sentences there is no need to search for similar sents. there is jus a limited number.
                fo.write(' BREAK '.join(nfl[i:i+n])+' BREAK '+''.join(fl[i])+'\n')
    f.close()
    fo.close()
# Remove tmp directory
subprocess.call(['rm','-rf', 'tmp'], shell=False)
