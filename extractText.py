#! /home/fantonio/anaconda2/bin/python
# -*- coding: utf-8 -*-
# Extracts text from aligned xml. 
# Script designed to work with https://wit3.fbk.eu/mt.php?release=2015-01 files
# Also generates a file with the dependencies of the sentences.
# fantoni[o|0] (20/03/18)
# It assumes the files are named like:
#       -training.l[1|2]
#       -dev.l[1|2]
#       -test.l[1|2]
import argparse
from xml.dom.minidom import parse, parseString
from lxml import etree

parser = argparse.ArgumentParser(description="Takes a route to the dataset files and extracts the sentences from seg tags.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Location")
parser.add_argument('-s', '--source', type=str, help = "Source Language")
parser.add_argument('-t', '--target', type=str, help = "Target Language")

args = parser.parse_args()
source =  args.source
target = args.target
dPath = args.dataset

for split in ['dev', 'test', 'training']:
    flink = open(split+'_link_samples.txt','w')        
    for st in [source, target]:
        fout = open(split+'.'+st,'w')
        print(dPath+'/'+split+'.'+st)        
        if split == 'dev':
            dom = parse(dPath+'/'+split+'.'+st)
            root = dom.getElementsByTagName("doc")
            for doc in root:        
                seg = doc.getElementsByTagName("seg");
                for s in seg:
                    fout.write(s.firstChild.wholeText.encode('utf8').strip()+'\n')
                    if st == source: flink.write(str(int(s.getAttribute("id"))-2).strip()+'\n')
        elif split == 'test':            
            for i in [0, 1, 2, 3]:
                dom = parse(dPath+'/IWSLT15.TED.tst201'+str(i)+'.'+source+'-'+target+'.'+st+'.xml')
                root = dom.getElementsByTagName("doc")
                for doc in root:        
                    seg = doc.getElementsByTagName("seg");
                    for s in seg:
                        fout.write(s.firstChild.wholeText.encode('utf8').strip()+'\n')
                        if st == source: flink.write(str(int(s.getAttribute("id"))-2).strip()+'\n')
        else: # trainining set
            idx = -1
            lines = open(dPath+'/'+split+'.'+st, 'r').readlines()[:-3]
            for i, l in enumerate(lines):
                if l[0] == '<':
                    idx = -1
                else:
                    if i == len(lines)-1:
                        fout.write(l.strip())
                    else:    
                        fout.write(l)
                    if st == source:
                        if i == len(lines)-1:
                            flink.write(str(idx))
                        else:
                            flink.write(str(idx)+'\n')
                        idx+=1







