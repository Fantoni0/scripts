#!/home/fantonio/miniconda2/bin/python
from keras_wrapper import dataset
import argparse
import sys

# Removes the following tokenization (see charTok.py for more info)
# # # # # e.g: hello --> hello|h_e_l_l_o 
# If the bpe flag is passed as argument it also detokenizes bpe
# # # # # e.g: sub@@|s_u_b_@_@ marine|m_a_r_i_n_e --> submarine
# fantoni[o|0] (4/6/18)

parser = argparse.ArgumentParser(description="Takes a route to a file and removes char .", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-fp', '--filePath', type=str, help="File Location")
parser.add_argument('--bpe', dest='bpe', action='store_true')
parser.add_argument('--no-bpe', dest='bpe', action='store_false')
parser.set_defaults(bo=False)

# Get arguments
args = parser.parse_args()
fPath = args.filePath
bpe = args.bpe

## Main ##
nameSplit = fPath.split('.')
name = ''.join(nameSplit[:-1])
extension = nameSplit[-1]
inputF = open(fPath, 'r')
outputF = open(name+'_charDetok.'+extension, 'w')
sentences = inputF.readlines()

for s in sentences:
    ns = ' '.join([unicode(w,'utf-8').split('|')[0] for w in s.split()])
    if bpe:
	ns = dataset.detokenize_bpe(ns)
    ns += '\n'
    outputF.write(ns.encode('utf-8'))

inputF.close()
outputF.close()
