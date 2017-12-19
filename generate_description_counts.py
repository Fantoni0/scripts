# Dummy script to generate number of descriptions (target sentences) that correspond to each source sentence
# It assumes one training sentence just have one reference.
# Useful when using conditional nmt (https://github.com/Fantoni0/TMA)
# fantoni[o|0]

import numpy as np

for split in ['training', 'dev', 'test']:
    fin = open('../'+split+'.en', 'r')
    if split == 'dev':
        fout = 'val_descriptions_counts.npy'
    elif split == 'training':
        fout = 'train_descriptions_counts.npy'
    else:
        fout = split+'_descriptions_counts.npy'
    np.save(fout, np.ones(len(fin.readlines()), dtype=int))
fin.close()
