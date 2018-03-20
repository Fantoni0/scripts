# Extracts text from aligned xml. 
# Script designed to work with https://wit3.fbk.eu/mt.php?release=2015-01 files
# Also generates a file with the dependencies of the sentences.
# fantoni[o|0] (20/03/18)

# It assumes the files are named like:
#       -training.l[1|2]
#       -dev.l[1|2]
#       -test.l[1|2]

import argparse
from xml.etree import cElementTree as ET 

parser = argparse.ArgumentParser(description="Takes a route to the dataset files and extracts the sentences from seg tags.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Location")
parser.add_argument('-s', '--source', type=str, help = "Source Language")
parser.add_argument('-t', '--target', type=str, help = "Target Language")


args = parser.parse_args()
source =  args.source
target = args.target
dPath = args.dataset

for split in ['training', 'dev', 'test']:
	for st in [source, target]:
		tree = ET.parse(dPath+'/'+split+'.'+st)
		root = tree.getroot()
		print(root)
		for child in root:
			print(child.tag, child.attrib)
