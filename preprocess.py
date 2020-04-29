import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--eos", action="store_true",
                    help="add . and <eos> to end of each example.")
parser.add_argument("--capitalize", action="store_true",
                    help="capitalize first character of each example.")
parser.add_argument("--evalsets", type=str, default=None, required=True,
                    help="directory containing evaluation sets to preprocess.")
args = parser.parse_args()

for filename in os.listdir(args.evalsets):
    if filename.endswith('.txt'):
        full_path = os.path.join(args.evalsets, filename)
        with open(full_path, 'r') as fin, open(full_path+'.p', 'w') as fout:
            for line in fin:
                gramm = line.split('\t')[0]
                sen = line.split('\t')[1]
                strip_line = sen.strip().split()
                if args.eos:
                    strip_line.append('.')
                    strip_line.append('<eos>')
                if args.capitalize:
                    strip_line[0] = strip_line[0].capitalize()
                fout.write(gramm + '\t' + ' '.join(strip_line) + '\n')
