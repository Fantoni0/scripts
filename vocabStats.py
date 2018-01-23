#!/home/anlarflo/miniconda2/bin/python
import argparse
import sys

# It computes different stats for a given dataset: n_sentences, n_words, size of vocabulary, out of vocabulary words, n_words per sentence, n_chars per word
# It works at word and character level. It measures both languages
# fantoni[o|0] (29/10/16)
'''
    It assumes the dataset files are in the form: training.l1, training.l2, dev.l1, dev.l2, test.l1, test.l2 
'''
parser = argparse.ArgumentParser(description="Takes a route to the dataset files and computes out-of-vocabulary words and some other measures.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ds', '--dataset', type=str, help="Dataset Location")
parser.add_argument('-s', '--source', type=str, help = "Source Language")
parser.add_argument('-t', '--target', type=str, help = "Target Language")
parser.add_argument('--character', dest='c', action='store_true')
parser.add_argument('--no-character', dest='c', action='store_false')
parser.add_argument('--shortmode', dest='sm', action='store_true')
parser.add_argument('--no-shortmode', dest='sm', action='store_false')
parser.add_argument('--print-oov', dest='po', action='store_true')
parser.add_argument('--no-print-oov', dest='po', action='store_false')
parser.set_defaults(c=False)
parser.set_defaults(sm=False)
parser.set_defaults(po=False)

#Short Mode only prints training set stats in one line

args = parser.parse_args()
source =  args.source
target = args.target
dPath = args.dataset
char = args.c
smode = args.sm
printo = args.po

#########################
###### FUNCTIONS ########
#########################
def muteText(text):
    nText = list()
    for w in text:
        for c in w:
            nText.append(c)
        nText.append('<space>')
    return nText

# Stats
oov = set()             # Words OOV
oovCounter = 0          # Number of OOV
sentences = 0           # Number of sentences
words = 0               # Number of words
vocabulary = 0          # Number of different words
wps = 0                 # Number of words per sentence
cpw = 0                 # Number of characters per word
trainingVocab = set()

for st in [source, target]:
    print("============================================ LANGUAGE:"+st+" =======================================")
    if not smode:
        print("{:10}\t {:10} \t {:10}\t {:10}\t {:10}\t {:2}\t {:2}".format("Set", "Sentences", "Words", "Vocabulary", "OOV", "WPS", "CPW"))
        print("================================================================================================")

    for f in ['training', 'dev', 'test']:
        currentF = open(dPath+'/'+f+'.'+st, 'r')
        sentences = len(currentF.readlines())
        currentF.close(); currentF = open(dPath+'/'+f+'.'+st, 'r')
        text = currentF.read().split()
        if char:
            text = muteText(text)
        words = len(text)
        vocabulary = len(set(text))
        wps = float(words)/sentences
        if len(text[0])<=1:
            cpw = float(sum([len(wo) for wo in text]))/words
        else:
            cpw = float(sum([len(wo.decode('utf-8')) for wo in text]))/words            
        if f == 'training': 
            trainingVocab = set(text)
        else:
            for w in text:
                if w not in trainingVocab:
                    oovCounter += 1
                    if w[-1]=='@':
                        oov.add("r\"("+w[:-2]+"\\w+)\"")
                    else:
                        oov.add(w)
        print("{:10}\t {:10} \t {:10}\t {:10}\t {:10}\t {:2.2f}\t {:2.2f}".format(f, sentences, words, vocabulary, oovCounter, wps, cpw))
        if smode: sys.exit()
        if printo and st == source and f == 'test':
            print(oov)
        oovCounter = 0
        oov = set()
    print("\n")

def muteText(text):
    return Dataset.tokenize_none_char(text)   
