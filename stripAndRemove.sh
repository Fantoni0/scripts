# It strips the xml from a text and removes the extra blank lines that appear as a result.
# It requires a moses script (strip-xml.perl) situated in mosesdecoder/scripts/general (add to the $PATH)
# fantoni[o|0] 6/7/2018

# Remove perl
strip-xml.perl <&0 > tmp.txt

# Remove blank lines
awk 'NF' < tmp.txt >&1

# Remove temporal file
rm tmp.txt
