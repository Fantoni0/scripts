# Wrapper to evaluate using multeval (https://github.com/jhclark/multeval)
# Requires to be in the same directory as multeval.sh (requires java)
# fantoni[o|0] (5/12/17)

if [ $# -lt 4 ]; then
    echo "Usage: `basename $0` references hypotheses language n_resamplings"
    echo "Evaluates machine translation ouput against a reference file"
    echo "example:`basename $0` test.es test.hyp es 3000"
    exit 1
fi

./multeval.sh eval --refs $1 \
                   --hyps-baseline $2 \
                   --meteor.language $3 \
		   --boot-samples $4
#		   --ar-shuffles $4 
#		   --rankDir rank
