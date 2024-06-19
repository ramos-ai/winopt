#!/bin/bash
# Usage:
#   eval_vs_human.sh <gold-file> <pred-file> <output-folder>
# ex:
# ../scripts/eval_vs_human.sh ../data/human_annotations/google.pt.csv ../data/human/google/pt/pt.pred.csv ../../results_eval_human
set -e

gold_fn=$1
pred_fn=$2
out_folder=$3


# Run evaluation
mkdir -p $out_folder/google/
out_file=$out_folder/google/pt.log
echo "Evaluating $lang into $out_file"
python eval_human.py --gold=$gold_fn --pred=$pred_fn > $out_file

echo "DONE!"
