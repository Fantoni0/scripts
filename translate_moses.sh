# Bash Script to translate a corpus using Moses.
# fantoni[o|0] (29/11/17)

# USAGE example:
# 	translate_moses.sh en fr europarl 5

# PARAMETERS:
#	$1 = SOURCE LANGUAGE (src)
#	$2 = TARGET LANGUAGE (trg)
#	$3 = CORPUS NAME
#	$4 = N-GRAM ORDER

# It assumes Moses, SRILM and GIZA are correctly installed. The following variables
# and path addings must be defined:
#	* export PATH=$PATH:/home/fantonio/tools/mosesdecoder/scripts/training:
#						/home/fantonio/tools/srilm/bin/i686-m64
#	* export MOSES=/home/fantonio/tools/mosesdecoder
#	* export SCRIPTS_ROOTDIR=/home/fantonio/tools/mosesdecoder/scripts
# 	* export GIZA=/home/fantonio/tools/bin

# It assumes a preprocessed corpus and the following folders and names estructure:
#	* training/
#		training.src
#		training.trg
#		*dev/
#			dev.src		
#			dev.trg		
#	*test/
#		test.src
#		test.trg

# START
# Get arguments
SRC_LAN=$1  # Source language
TRG_LAN=$2  # Target language
CORPUS=$3   # Corpus name
ORDER=$4    # N-gram order (5 by default)
# Clean train set. Delete sentences longer than 70 words
clean-corpus-n.perl training/training $SRC_LAN $TRG_LAN training/training.clean 1 70

# Create language model using SRILM
cd training/
rm -rf lm					# Remove old directory
mkdir lm
ngram-count -order $ORDER -unk -interpolate -kndiscount \
 -text training.clean.$TRG_LAN -lm lm/$CORPUS.lm
echo "Language model created"

# Create phrase and reorder tables (translation model)
rm -rf work					# Remove old directory
rm -rf mert-work				# Remove old directory

$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir work \
 -corpus training.clean -f $SRC_LAN -e $TRG_LAN \
 -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
 -lm 0:$ORDER:$PWD/lm/$CORPUS.lm -external-bin-dir $GIZA --parallel > training.out

# Train log-lineal weights (MERT)
clean-corpus-n.perl dev/dev $SRC_LAN $TRG_LAN dev/dev.clean 1 70  # Clean dev set
cd ../
$MOSES/scripts/training/mert-moses.pl \
 training/dev/dev.clean.$SRC_LAN training/dev/dev.clean.$TRG_LAN \
 $MOSES/bin/moses training/work/model/moses.ini\
 --maximum-iterations=5 \
 --mertdir $MOSES/bin/ \
 --threads=4 \
 --decoder-flags "-feature-name-overwrite \"SRILM KENLM\""

sed ":a;N$bash;s/\"SRILM\nKENLM/\"SRILM KENLM\"/" mert-work/moses.ini > mert-work/moses.$CORPUS.ini

# Translation process
cd test/
$MOSES/bin/moses --threads 4 -feature-name-overwrite "SRILM KENLM" \
 -f ../mert-work/moses.$CORPUS.ini < test.$SRC_LAN > test.hyp  # Remove --threads when using RIGEL UPV



