# Simple script to remove the worst models of a training. This is done to save space.
# Requires coco_sort.sh (https://github.com/Fantoni0/scripts)
# Sorts by Bleu. By default all models are removed except from the best 3.
# Parameters:
#    $1: Folder with the model files.
#    $2: Number of models to save.
# fantoni[o|0] (26/11/18)

if [ $# -lt 1 ]; then
    echo "Usage: `basename $0` folder [n_models_to_save] "
    echo "Removes all models except the n_models_to_save best to save disk space"
    echo "Example: removeWorstModels.sh ted-enfr-transformer/ 3"
    exit 1
fi 

if [ $# -lt 2 ]; then
    n_models=3
else
    n_models=$2
fi
coco_sort.sh $1/val.coco | tail -n +$((${n_models}+1)) | cut -d "," -f 1 | while read -r line; do
    rm -f $1/epoch_${line}_*
    rm -f $1/epoch_${line}.h5
    rm -f $1/update_${line}_*
    rm -f $1/update_${line}.h5
done
rm -f $1/epoch_*
