#!/bin/bash
#SBATCH --job-name=eval_lm_he
#SBATCH --time=47:59:59
#SBATCH --partition=gpuk80
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=6
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --mail-type=end
#SBATCH --mail-user=amuelle8@jhu.edu
#SBATCH --output=/home-1/amuelle8@jhu.edu/logs/out-eval-$2.log
#SBATCH --error=/home-1/amuelle8@jhu.edu/logs/err-eval-$2.log

# USAGE: ./test.sh <evalset_directory> <model_directory> <test_case>

module load cuda/9.0
source /home-1/amuelle8@jhu.edu/miniconda3/bin/activate
LD_LIBRARY_PATH=/home-1/amuelle8@jhu.edu/miniconda3/lib:$LD_LIBRARY_PATH
PATH=/home-1/amuelle8@jhu.edu/miniconda3/bin:$PATH
conda activate for_pytorch
# source ../hyperparameters.txt

model_name=`basename $2`

if [ "$3" = "all" ]; then
	for file in `ls $1`; do
		if [[ $file == *".txt" ]]; then
			echo "Processing $file"
			python test.py \
				--test \
				--lm_data $1 \
				--cuda \
				--save $2/lstm_lm.pt \
				--save_lm_data $2/lstm_lm.bin \
				--testfname $file \
				--words > $1/${file}.${model_name}.wordscores
		fi
	done
else
	echo "Processing $file"
	python test.py \
		--test \
		--lm_data $1 \
		--cuda \
		--save $2/lstm_lm.pt \
		--save_lm_data $2/lstm_lm.bin \
		--testfname $3 \
		--words > $1/${3}.${model_name}.wordscores
fi

#python test.py \
#    --test \
#    --lm_data $1 \
#	--cuda \
#    --save $2 \
#    --testfname $3 \
#    --words > $1/$3.wordscores
