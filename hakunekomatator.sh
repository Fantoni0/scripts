# Script to convert jpg manga files to PDF files.
# The script assumes you used the HakuNeko downloader (https://hakuneko.download/) to obtain the manga files. Therefore it expects a folder for each chapter with jpg numerical names.
# Fantoni[o|0] (10/06/2023)

# Arguments
# manga_directory: Where the manga chapters are stored
# chapter_bundle: Bundles n individuals chapters as a single PDF. Default value is 20.
# remove_page: ...remove page(s) number.

if [ $# -lt 1 ]; then
    echo "Usage: `basename $0` manga_directory [chapter_bundle] [remove_page]"
    echo "Com"
    echo "example:`basename $0` test.es test.hyp es 3000"
    exit 1
fi

working_dir=$1


if [[ $# -lt 2 ]];
then
    chapter_bundle=20

else
    chapter_bundle=$2
fi


if [[ $# -lt 3 ]];
then
    remove_page=00

else
    remove_page=$3
fi


# Create output directory
out_dir=${working_dir}/PDF
rm -rf ${working_dir}/PDF
rm chap_list.txt
mkdir -p ${out_dir}
mkdir -p ${out_dir}/single_chapters
mkdir -p ${out_dir}/bundled_chapters

if [ "$(ls -A ${out_dir}/single_chapters)" ]; then
     echo "single_chapters directory is not empty. No individual chapters will be generated."
else
    # Convert chapters from set of JPG images to PDF
    find $working_dir -maxdepth 1 -type d -not -path "./PDF" -not -path "." | sort  -V | while read IN;
    do
    cd "$IN"
    convert $(find . -regex ".*\.\(jpg\|\png\|jpeg\)"  ! -name ${remove_page}".jpg" | sort) ../PDF/single_chapters/"$IN".pdf;
    cd ..
    echo "$IN".pdf >> chap_list.txt
done
fi

# Bundle chapters together
cd ./PDF/single_chapters/
i=1
while mapfile -t -n $chapter_bundle ary && ((${#ary[@]})); do
    echo "${ary[@]}"
    pdfunite "${ary[@]}" ../bundled_chapters/$i.pdf
    echo $i
    i=$((i+1))
    echo $i
done < ../../chap_list.txt

echo "DONE"