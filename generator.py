import sys
import os
import argparse
from grammar import Grammar


parser = argparse.ArgumentParser()
parser.add_argument("--check_vocab", type=str, default=None,
                    help="location of vocab file to check entries against")
parser.add_argument("--grammars", type=str, help="directory containing grammars")
args = parser.parse_args()

assert os.path.isdir(args.grammars)
if args.grammars.endswith('/'):
    args.grammars = args.grammars[:-1]

grammar = Grammar(args)

for filename in os.listdir(args.grammars):
    if filename.endswith('common.avg'):
        continue
    grammar = Grammar(args)
    grammar.read(os.path.join(args.grammars,'common.avg'))
    grammar.read(os.path.join(args.grammars,filename))
    if not os.path.isdir(args.grammars+'_evalset'):
        os.mkdir(args.grammars+'_evalset')
    grammar.sen_generate(os.path.join(args.grammars+'_evalset', os.path.basename(filename).split(".")[0]+".txt"))
