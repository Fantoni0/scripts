#!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It concatenates previous sentences and current sentences in one line: prev BREAK curr
# It searches for the most similar sentence to prepend
# REQUIRES gensim
# fantoni[o|0] (23/7/18)

# Similar to generateSimilarConcatenatedCorpus.py
# It does not enforce the requirement of preprending a previous sentence. It appends the most similar one (it can be ahead)

import argparse
import subprocess
import gensim
import os
import collections
import smart_open
import random

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''

parser = argparse.ArgumentParser(description="Takes a route to the dataset files and preprends the most similar(past) sentence to each sentence", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Locations")
parser.add_argument('-ps', '--prev_sentences', type=int, help="Number of sentences to concatenate")
parser.add_argument('-ns', '--next_sentences', type=int, help="Number of sentences to concatenate")
parser.add_argument('-pt', '--prev_sentences2', type=int, help="Number of sentences to concatenate")
parser.add_argument('-nt', '--next_sentences2', type=int, help="Number of sentences to concatenate")
parser.add_argument('-s', '--source', type=str, help="Source language of the splits")
parser.add_argument('-t', '--target', type=str, help="Target languages of the split. Use the same order as in datasets")

# Get parameters
args = parser.parse_args()
dataset =  args.dataset
ns = args.next_sentences
ps = args.prev_sentences
nt = args.next_sentences2
pt = args.prev_sentences2
source = args.source
target = args.target


## Function definitions
# Read function from --> https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/doc2vec-lee.ipynb
def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

## MAIN
# Create Folder
folderName = 'similarDoc2VecConcatenated-ps%d-ns%d-pt%d-nt%d' % (ps, ns, pt, nt)
createFolder = ['mkdir','-p', '%s/%s' % (dataset, folderName)]
subprocess.call(createFolder, shell=False)

# Concatenate sentences
for idx, s in enumerate(['test', 'training', 'dev']): # Do not apply concatenation to test set
    print("Start process on %s parition" % (s)) 
    # Open source and destination files. For both, source and target languages.
    f_source = open(dataset+'/'+s+'.'+ source, 'r')
    f_target = open(dataset+'/'+s+'.'+ target, 'r')
    fo_source = open(dataset+'/'+folderName+'/'+s+'.'+ source, 'w')
    fo_target = open(dataset+'/'+folderName+'/'+s+'.'+ target, 'w')    
    
    # Read lines
    train_corpus = list(read_corpus(dataset+'/'+s+'.'+ source))
    test_corpus = list(read_corpus(dataset+'/'+s+'.'+ source, tokens_only=True))
    
    fl_source = f_source.readlines()
    fl_source = [line.strip() for line in fl_source] # Remove \n 
    gensim_tokenized_source = [ ' '.join(gensim.utils.simple_preprocess(line)) for line in fl_source]
   
    fl_target = f_target.readlines()
    fl_target = [line.strip() for line in fl_target] # Remove \n

    # Train Model
    model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=2, epochs=40)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    
    # Get the most similar sentences.
    for i in range(len(train_corpus)):
        prev_source = []
        prev_target = []
        inferred_vector = model.infer_vector(test_corpus[i])
        sims = model.docvecs.most_similar([inferred_vector], topn=ps+1)
        ref_sent = ' '.join(test_corpus[i])
        for j in range(ps):
            sim_sent = ' '.join(train_corpus[sims[j+1][0]].words)
            idx_target = gensim_tokenized_source.index(sim_sent)
            prev_source.append(fl_source[idx_target])
            prev_target.append(fl_target[idx_target])
        
        # Forward context
        next_source = fl_source[i+1:min(len(fl_source), i+1+ns)] + ['<pad>'] * ( (i+1) - len(fl_source) + ns)
        next_target = fl_target[i+1:min(len(fl_target), i+1+nt)] + ['<pad>'] * ( (i+1) - len(fl_target) + nt)               
        # Write
        fo_source.write(' BREAK '.join(prev_source)+ ' BREAK ' + fl_source[i] + ' BREAK '*(len(next_source)>0) + ' BREAK '.join(next_source) + '\n')        
        fo_target.write(' BREAK '.join(prev_target)+ ' BREAK ' + fl_target[i] + ' BREAK '*(len(next_target)>0) + ' BREAK '.join(next_target) + '\n')
    f_source.close()
    f_target.close()
    fo_source.close()
    fo_target.close()
