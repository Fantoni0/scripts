# Script for generating linked list of translation dependencies
# Useful when using conditional nmt (https://github.com/Fantoni0/TMA)
# fantoni[o|0] (7/12/17)

# It assumes the files are named like:
#	-training.l[1|2]
#	-dev.l[1|2]
#	-test.l[1|2]

for split in ['training', 'dev', 'test']:
    fin = open('../'+split+'.en', 'r')
    if split == 'dev':
        fout = open('val_link_samples.txt', 'w')
    elif split == 'training':
        fout = open('train_link_samples.txt', 'w')
    else:
        fout = open(split+'_link_samples.txt', 'wr')
    fout.write("-1\n")
    for l in range(len(fin.readlines())-1):
        fout.write(str(l)+"\n")
fin.close()
fout.close()
