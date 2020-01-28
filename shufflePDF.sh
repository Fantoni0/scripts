# Simple script to shuffle pdf pages in scanned documents.
# My HP (Damn you HP, hearthless company) scanner does not support both-sides scanning. I have to run the document first on one side, then in the other one.
# To the best of my knowledge, in linux there is no support to automatically intercalate pages. This script aims to solve that problem.
# Example: My scanner produces this output for a N pages doc with text in both sides (face A and B):
# 		1_A 2_A 3_A ... N_A N_B ... 3_B 2_B 1_B
# This script rearranges the pages:
#		1_A 1_B 2_A 2_B 3_A 3_B ... N_A N_B
# It uses pdfseparate and pdfunite. Both supported in ubuntu.
# It takes a list of pdf files to modify as argument.
# Fantoni[o|0] (21/01/2020)

for arg in "$@"
do
	mkdir .tmp
	cp ${arg} .tmp/
	cd .tmp
	pdfseparate ${arg} %d.pdf
	rm ${arg}
	names=()
	num=$(ls | wc -l)
	hnum=$((${num}/2 - 1))
	for i in $(seq 0 $hnum)
	do
		names="${names}$((i+1)).pdf "
		names="${names}$(($num-$i)).pdf "
	done
	pdfunite ${names} shuffled_${arg}
	cp shuffled_${arg} ../
	cd ..
	rm -rf .tmp/
done	
