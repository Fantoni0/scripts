# -*- coding: utf-8 -*-
# It computes the average/median/mode length of a dataset
# fantoni[o|0] (4/7/17)

import argparse
import sys
import operator

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes average length of sentences and words", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Location")
parser.add_argument('-s', '--source', type=str, help = "Source Language")
parser.add_argument('-t', '--target', type=str, help = "Target Language")

#Short Mode only prints training set stats in one line

args = parser.parse_args()
source =  args.source
target = args.target
dPath = args.dataset

#########################
###### FUNCTIONS ########
#########################
def getMedianMode(data):
    # Build Histogram
    hist = dict()
    for d in data:
        if not hist.get(len(d), False):
            hist[len(d)] = 1
        else:
            hist[len(d)] += 1
    # Median
    sortHist = sorted(hist.items(), key=operator.itemgetter(0))
    acc = median = 0
    for k,v in sortHist:
        acc += hist[k]
        if acc / float(len(data)) >= 0.5:
            median = k
            break      
    # Mode
    mode = sorted(hist.items(), key=operator.itemgetter(1))[-1][0]
    #print(hist) 
    return median, mode      


# Stats

print("{:10}\t {:10} \t {:10} \t {:10} \t {:10} \t {:10} \t {:10} ".format("Set", "Avg. Sentences", "Avg. Words", "Median Sent.", "Median Word.", "Mod Sent.", "Mod Word."))
print("==================================================================================================================")
for f in ['training', 'dev', 'test']:
    currentF = open(dPath+'/'+f+'.'+source, 'r')
    sentences = currentF.readlines()
    sentences = [s.split() for s in sentences]
    lengthSent = sum([len(l) for l in sentences])/float(len(sentences))
    medSent, modSent = getMedianMode(sentences)
    currentF.close(); currentF = open(dPath+'/'+f+'.'+source, 'r')
    text = currentF.read().split()
    text = [t.decode('utf-8') for t in text]
    medWord, modWord = getMedianMode(text)
    lengthWord = sum([len(w) for w in text])/float(len(text))
    print("{:10}\t {:.2f}\t\t\t {:.2f} \t\t {:2d} \t\t {:2d} \t\t {:2d} \t\t {:2d} ".format(f, lengthSent, lengthWord, medSent, medWord, modSent, modWord ))

