#!/home/fantonio/miniconda2/bin/python
import argparse
import sys

# It appends each word of the dataset its character representation concatenated. Eg: hello --> hello|h_e_l_l_o 
# By default it only applies such "tokenization" to the source side. If the --both option is passed as argument it will be applied to source and target languages. 
# fantoni[o|0] (31/5/18)

# TODO: It should be able to automatically create the folder (look for os python library)
# TODO: It should copy untouched files into the new folder (subprocess library should do the job)
'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes out-of-vocabulary words and some other measures.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Location")
parser.add_argument('-s', '--source', type=str, help = "Source Language")
parser.add_argument('-t', '--target', type=str, help = "Target Language")
parser.add_argument('--both', dest='bo', action='store_true')
parser.add_argument('--no-both', dest='bo', action='store_false')
parser.set_defaults(bo=False)

# Get arguments
args = parser.parse_args()
source =  args.source
target = args.target
dPath = args.dataset
both = args.bo

## Functions ##
def tokSentence(sentence):
    outsentence = ""
    for w in sentence.split():
	w = unicode(w,'utf-8')
        outsentence += w+u'|'
        for c in w:
            outsentence += c+u'_'
        outsentence = outsentence[:-1]  # Remove last _
        outsentence += ' '
    return outsentence.strip()+'\n'

## Main ##
sides = [source, target] if both else [source]
for st in sides:
    for f in ['training', 'dev', 'test']:
        currentF = open(dPath+'/'+f+'.'+st, 'r')
        targetF = open(dPath+'/plusChar/'+f+'.'+st, 'w')
        sentences = currentF.readlines()
        for s in sentences:
            targetF.write(tokSentence(s).encode('utf-8'))
        currentF.close();
        targetF.close();
