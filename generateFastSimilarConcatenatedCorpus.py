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
parser.add_argument('-m', '--model', type=str, help="Pre-trained model. Optional argument.")

# Get parameters
args = parser.parse_args()
dataset =  args.dataset
n = args.sentences
source = args.source
target = args.target
model = args.model

b_model = model != None
print("Using pretrained model? = ", b_model)

# Create Folder
folderName = 'similarFastConcatenated-%d' % n 
createFolder = ['mkdir','-p', '%s/%s' % (dataset, folderName)]
subprocess.call(createFolder, shell=False)
subprocess.call(['mkdir','-p', 'tmp'], shell=False) # Create tmp directory

# Concatenate sentences
for idx, s in enumerate(['test', 'training', 'dev']): # Do not apply concatenation to test set
    print("Start process on %s parition" % (s)) 
    # Open source and destiantion files. For both, source and target languages.
    f_source = open(dataset+'/'+s+'.'+ source, 'r')
    f_target = open(dataset+'/'+s+'.'+ target, 'r')
    fo_source = open(dataset+'/'+folderName+'/'+s+'.'+ source, 'w')
    fo_target = open(dataset+'/'+folderName+'/'+s+'.'+ target, 'w')    
    # Get lines
    fl_source = f_source.readlines()
    fl_target = f_target.readlines()
    fl_source = [line.strip() for line in fl_source] # Remove \n 
    fl_target = [line.strip() for line in fl_target] # Remove \n
    nfl_source = n*['<pad>'] + fl_source
    nfl_target = n*['<pad>'] + fl_target

    # No need to train the model if we are using a pretrained one.
    if not b_model:
        # Train Model using sent2vec
        subprocess.call(['fasttext', 'sent2vec', '-input', '%s.%s' % (s, source), '-output', 'tmp/model_%s_%s' % (s, source), '-epoch', '10', '-lr', '0.2', '-wordNgrams', '5', '-loss', 'ns', '-neg', '10', '-thread', '20', '-t', '0.00005', '-dropoutK', '6', '-bucket', '6000000'], shell=False)

    # Get most similar sentences in an output file
    with open(dataset+'/'+s+'.'+source, 'r') as infile:
        with open(dataset+'/tmp/out.txt', 'w') as outfile:
            if b_model:
                print("Using pretrained model.")
                subprocess.call(['fasttext', 'nnSent', model, '%s.%s' % (s,source) , '%d' % (n+1)],stdin=infile, stdout=outfile, shell=False)
            else:
                subprocess.call(['fasttext', 'nnSent', dataset+'/tmp/model_%s_%s.bin' % (s,source), '%s.%s' % (s,source) , '%d' % (n+1)],stdin=infile, stdout=outfile, shell=False)
                
    # Get the n most similar sentences
    fo2 = open('tmp/out.txt','r')
    fl2_source = fo2.readlines()[1:-1] # Remove first line, contains log information. Last line is a \n
    fl2_source = [line.strip() for line in fl2_source if line!='\n'] # Remove lines containing just \n and trim the others
    
    # Get the index of the extracted senteces. We want the same sentences in the target side
    fl2_target = []
    for sen in fl2_source:
        index = fl_source.index(' '.join(sen.split()[2:]))
        fl2_target.append(fl_target[index])        
    # Write 
    j = 1    
    for i in range(len(fl_source)):
        print(fl2_source[j:j+n])
        print(fl2_target[j:j+n])
        #print("The Join: ", [' '.join([ll2.split()[2:] for ll2 in fl2[j:j+n]][0])])
        fo_source.write(' BREAK '.join([' '.join([ll2.split()[2:] for ll2 in fl2_source[j:j+n]][0])])+' BREAK '+''.join(fl_source[i])+'\n')
        fo_target.write(' BREAK '.join([' '.join([ll2.split() for ll2 in fl2_target[j:j+n]][0])])+' BREAK '+''.join(fl_target[i])+'\n')
        j = i + n
    fo_source.close()
    fo_target.close()
    fo2.close()
# Remove tmp directory
subprocess.call(['rm','-rf', 'tmp'], shell=False)
