import argparse
import pickle
import os
import subprocess
import operator
import logging
from tester.TestWriter import TestWriter
from template.TestCases import TestCase

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Parameters for testing a language model")

parser.add_argument('--template_dir', type=str, default='eval_templates',
                    help='Location of the template files')
parser.add_argument('--sentence_file', type=str, default='all_test_sents.txt',
                    help='File to store all of the sentences that will be tested')
parser.add_argument('--output_file', type=str, required=True,
                    help='Name of the output file (default: model name)')
parser.add_argument('--model_type', type=str, default='rnn',
                    choices=['rnn', 'tf'],
                    help='type of model to eval')
args = parser.parse_args()

#if args.output_file == None:
#    args.output_file = '.'.join(args.model.split('/')[-1].split('.')[:-1])+'.output'

writer = TestWriter(args.template_dir, args.sentence_file)

# Read tests
writer.read_tests()

name_lengths = writer.name_lengths
key_lengths = writer.key_lengths

if args.model_type == 'rnn':
    scoring_indices = [0,1,4]
elif args.model_type == 'tf':
    scoring_indices = [0,1,2]

def test_LM():
    logging.info("Testing Model Output...")
    results = score_rnn()
    with open('.'.join(args.output_file.split('.')[:-1]) + "_results.pickle", 'wb') as f:
        pickle.dump(results, f)

def score_rnn():
    logging.info("Scoring Model Output...")
    with open(args.output_file, 'r') as f:
        all_scores = {}
        first = False
        score = 0.
        sent = []
        prev_sentid = str(-1)
        for line in f:
            if not first:
                first = True
            elif "===========================" in line:
                break
            else:
                wrd, sentid, wrd_score = [line.strip().split()[i] for i in scoring_indices]
                score = -1 * float(wrd_score) # multiply by -1 to turn surps back into logprobs
                sent.append((wrd, score))
                if wrd == ".":
                    name_found = False
                    for (k1,v1) in sorted(name_lengths.items(), key=operator.itemgetter(1)):
                        if float(sentid) < v1:
                            if k1 not in all_scores:
                                all_scores[k1] = {}
                            key_found = False
                            for (k2,v2) in sorted(key_lengths[k1].items(), key=operator.itemgetter(1)):
                                if int(sentid) < v2:
                                    if k2 not in all_scores[k1]:
                                        all_scores[k1][k2] = []
                                    all_scores[k1][k2].append(sent)
                                    break
                            break
                    sent = []
                    if float(sentid) != float(prev_sentid)+1:
                        logging.info("Error at sents "+sentid+" and "+prev_sentid)
                    prev_sentid = sentid
    return all_scores

def clean_files(mode):
    os.system('rm rnn.output')

test_LM()
