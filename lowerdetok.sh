# Script to lowercase and tokenize a corpus using moses scripts
# Requires Moses
# fantoni[o|0]
if [$# -lt 2]; then
	echo "Usage: `basename $0` file language"
	echo "Example: lowerdetok.sh training.de de"
	exit 1
fi

moses=/home/fantonio/software/mosesdecoder/scripts/tokenizer

mkdir lowercased
${moses}/lowercase.perl -l $2 < $1 > tmp.txt
${moses}/tokenizer.perl -l $2 -no-escape < tmp.txt > lowercased/$1
rm tmp.txt
