!/home/fantonio/miniconda2/bin/python
# -*- coding: utf-8 -*-
# It extracts N random lines from M files. Creating N*M set files
# fantoni[o|0] (4/7/17)

import argparse
import sys
import operator
import random

'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes average length of sentences and words", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, nargs='+', help="Dataset Locations")
parser.add_argument('-n', '--lines', type=int, nargs='+', help="Number of lines to extract from each split")

'''
    Example of usage:
        python extractSplits.py -ds xerox/enfr xerox/enes xerox/ende -n 10000 300 250
   
    It will extract 10000 random lines from xerox/enfr/training.[en|fr], xerox/enes/training.[en|es] and xerox/ende/training.[en|de] and it will store them in ./training.[src|trg]
    It will extract 300 random lines from xerox/enfr/dev.[en|fr], xerox/enes/dev.[en|es] and xerox/ende/dev.[en|de] and it will store them in ./dev.[src|trg]
    It will extract 250 random lines from xerox/enfr/test.[en|fr], xerox/enes/test.[en|es] and xerox/ende/test.[en|de] and it will store them in ./test.[src|trg]
'''

#Short Mode only prints training set stats in one line

args = parser.parse_args()
datasets =  args.dataset
lines = args.lines
for idx, s in enumerate(['training', 'dev', 'test']):        
        for d in enumerate(datasets):
            source = d[-4:-2]
            target = d[-2:]
            eval(source+'_'+'_lines') = []                
            tar_lines = []                
            rindexes = random.sample([i for i in xrange(lines[idx])], lines[idx])
            for l in [source, target]:                      
                f = open(ds+'/'+s+'.'+l, 'r')
                fl = f.readlines()                
                fl = [fl(i) for i in rindexes]
                if l in eval(source+'_'+'_lines'):
                    eval(source+'_'+'_lines').append(fl) 
                else:
                    tar_lines =append(fl)
                f.close()
        fout1 = (s+'.src','a')
        fout2 = (s+'.trg','a')
        fout1.write(eval(source+'_'+'_lines'))
        fout2.write(tar_lines)
        fout1.close()
        fout2.close()
        

        


        
        
