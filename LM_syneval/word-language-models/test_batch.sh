#!/bin/bash
#SBATCH --job-name=eval_ru
#SBATCH --time=47:59:59
#SBATCH --partition=gpuk80
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=6
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --mail-type=end
#SBATCH --mail-user=amuelle8@jhu.edu
#SBATCH --output=/home-1/amuelle8@jhu.edu/logs/out-eval-ru.log
#SBATCH --error=/home-1/amuelle8@jhu.edu/logs/err-eval-ru.log

# USAGE: ./test.sh <evalset_directory> <lm.pt> <lm.bin> <test_case>

module load cuda/9.0
source /home-1/amuelle8@jhu.edu/miniconda3/bin/activate
LD_LIBRARY_PATH=/home-1/amuelle8@jhu.edu/miniconda3/lib:$LD_LIBRARY_PATH
PATH=/home-1/amuelle8@jhu.edu/miniconda3/bin:$PATH
conda activate for_pytorch
# source ../hyperparameters.txt

if [ "$4" = "all" ]; then
	for file in `ls $1`; do
		if [[ $file == *".txt" ]]; then
			echo "Processing $file"
			python test.py \
				--test \
				--lm_data $1 \
				--cuda \
				--save $2 \
				--save_lm_data $3 \
				--testfname $file \
				--words > $1/$file.wordscores
		fi
	done
else
	echo "Processing $file"
	python test.py \
		--test \
		--lm_data $1 \
		--cuda \
		--save $2 \
		--save_lm_data $3 \
		--testfname $4 \
		--words > $1/$4.wordscores
fi

#python test.py \
#    --test \
#    --lm_data $1 \
#	--cuda \
#    --save $2 \
#    --testfname $3 \
#    --words > $1/$3.wordscores
