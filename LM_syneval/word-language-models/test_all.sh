#!/bin/bash

# USAGE: ./test_all.sh <language_code>
# loops through all models of a given language, tests performance on evalsets

for model_dir in `ls -d ../models/${1}1.*`; do
	eval_dir="../../eval_sets/${1}_replication_evalset_2"
	echo "Evaluating `basename $model_dir` on `basename $eval_dir`"
	sbatch ./test.sh $eval_dir $model_dir all
done
