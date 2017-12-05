import re
import argparse

# Given a list of BPE tokens searches how many words contain them in a file.
# Intended to search OOV, at word level, in a test file given BPE tokens.
# fantoni[o|0]
parser = argparse.ArgumentParser(description="Takes a route to  files and computes out-of-vocabulary words.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-f', '--filel', type=str, help="File location")

args = parser.parse_args()
route = args.filel
bpe_tokens = ['punkt']  # Modify list of BPR tokens to search. TODO: Load list as argument/from file. 

test_file = open(route, 'r')
oov = 0
oovd = dict()
words = set()
for l in test_file.readlines():
    for w in l.split():
        for t in bpe_tokens:
            if re.search(t, w):
                oov += 1
                if w not in oovd:
                    oovd[w]=1
                else:
                    oovd[w]+=1
                words.add(w)
                break # Special case. A word with two bpe_tokens should be counted as just one OOV
print(words)
print(len(words))
print(oov)
print(oovd)
