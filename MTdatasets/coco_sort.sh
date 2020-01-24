# Simple script to sort values from nmt-keras (https://github.com/lvapeab/nmt-keras)
# Sorts by the fifth column (Bleu_4) value
# fantoni[o|0] (26/6/16)

tail -n +2 $1 | sort -r -t ',' -k 5
