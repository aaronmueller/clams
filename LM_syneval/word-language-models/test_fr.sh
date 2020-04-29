#!/bin/bash
source /home/amueller/miniconda3/bin/activate
conda activate pytorch
export CUDA_VISIBLE_DEVICES=`free-gpu`
export LD_LIBRARY_PATH=/opt/NVIDIA/cuda-9.0/lib64

python main.py --test --lm_data ../../LM_marcc/fr_data --save ../../LM_marcc/models/fr1/lstm_lm.pt --save_lm_data ../../LM_marcc/models/fr1/lstm_lm.bin
