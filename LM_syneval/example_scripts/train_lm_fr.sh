#!/bin/bash
#SBATCH --job-name=train_lm_fr.$SLURM_JOBID
#SBATCH --time=47:59:59
#SBATCH --partition=gpuk80
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=6
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --mail-type=end
#SBATCH --mail-user=amuelle8@jhu.edu
#SBATCH --output=/home-1/amuelle8@jhu.edu/logs/out-lstm-fr.$SLURM_JOBID.log
#SBATCH --error=/home-1/amuelle8@jhu.edu/logs/err-lstm-fr.$SLURM_JOBID.log
#SBATCH --workdir=/home-1/amuelle8@jhu.edu/scratch/workdir/fr.$SLURM_JOBID
module load cuda/9.0
source /home-1/amuelle8@jhu.edu/miniconda3/bin/activate
PATH=/home-1/amuelle8@jhu.edu/miniconda3/bin:$PATH
LD_LIBRARY_PATH=/home-1/amuelle8@jhu.edu/miniconda3/lib:$LD_LIBRARY_PATH
conda activate for_pytorch

source /home-1/amuelle8@jhu.edu/scratch/LM_syneval/hyperparameters_fr.txt
mkdir -p ${model_dir}.$SLURM_JOBID

python3 -u $lm_dir/main.py \
       --lm_data $lm_data_dir \
       --cuda \
       --epochs $epochs \
       --model $model \
       --nhid $num_hid \
       --save ${model_dir}.$SLURM_JOBID/lstm_lm.pt \
       --save_lm_data ${model_dir}.$SLURM_JOBID/lstm_lm.bin \
       --log-interval $log_freq \
       --batch $batch_size \
       --dropout $dropout \
	   --seed $SLURM_JOBID \
       --lr $lr \
       --trainfname $train \
       --validfname $valid \
       --testfname $test
