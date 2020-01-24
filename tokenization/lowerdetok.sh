# Script to lowercase and tokenize a corpus using moses scripts
# Requires Moses
# fantoni[o|0]
if [ $# -lt 3 ]; then
	echo "Usage: `basename $0` folder file language"
	echo "Example: lowerdetok.sh data/ training.de de"
	exit 1
fi

moses=/home/fantonio/software/mosesdecoder/scripts/tokenizer

mkdir -p lowercased
${moses}/lowercase.perl -l $3 < $1/$2 > tmp.txt
${moses}/tokenizer.perl -l $3 -no-escape < tmp.txt > nmtTok/$2
rm tmp.txt
