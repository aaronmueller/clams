import os
import argparse
import statistics

parser = argparse.ArgumentParser(description="Analyze results of LM tested on hand-crafted evaluation sets")

parser.add_argument('--score_dir', type=str, default=None,
                    help='location of the directory containing word scores')
parser.add_argument('--case', type=str, default='all',
                    help='which evaluation cases to get accuracies for')
parser.add_argument('--word_compare', action='store_true',
                    help='compare target word scores instead of full sentence scores')

args = parser.parse_args()


def do_word_compare(scorefile, scoredict, case):
    grammatical_sentid = 0
    grammatical_sent = []
    grammatical_surps = []
    prev_grammatical = False
    more_probable = True
    correct = 0.
    total = 0.

    if case not in scoredict.keys():
        scoredict[case] = []

    for line in scorefile:
        if line.startswith('word sentid sentpos'):
            continue
        elif line.startswith('===================='):
            if more_probable:
                correct += 1.
            total += 1.
            scoredict[case].append(correct / total)
            break
        elif not line.strip():
            continue
        
        line_tuple = line.strip().split()
        word = line_tuple[0]
        sentid = int(line_tuple[1])
        sentpos = int(line_tuple[2])
        surprisal = float(line_tuple[4])
        if line_tuple[6] == "True":
            is_grammatical = True
        else:
            is_grammatical = False

        if is_grammatical:
            if sentpos == 0:    # clear array, reset variables
                if prev_grammatical:
                    print("Error: two consecutive grammatical sentences!")
                    print(grammatical_sent)
                    scoredict[case].append(0.)
                    return
                prev_grammatical = True
                if more_probable:
                    correct += 1.
                total += 1.
                grammatical_sent = []
                grammatical_surps = []
                more_probable = True
            grammatical_sentid = sentid
            grammatical_sent.append(word)
            grammatical_surps.append(surprisal)

        else:
            if sentpos == 0:
                prev_grammatical = False
            if word != grammatical_sent[sentpos]:   # this is the word we vary
                if surprisal < grammatical_surps[sentpos]:
                    more_probable = False


def do_sen_compare(scorefile, scoredict, case):
    grammatical_sentid = 0
    grammatical_surp = 0.
    prev_grammatical = False
    more_probable = True
    correct = 0.
    total = 0.
    ungrammatical_surp = 0.

    if case not in scoredict.keys():
        scoredict[case] = []

    for line in scorefile:
        if line.startswith('word sentid sentpos'):
            continue
        elif line.startswith('===================='):
            if more_probable and grammatical_surp <= ungrammatical_surp:
                correct += 1.
            total += 1.
            scoredict[case].append(correct / total)
            break
        elif not line.strip():
            continue

        line_tuple = line.strip().split()
        word = line_tuple[0]
        sentid = int(line_tuple[1])
        sentpos = int(line_tuple[2])
        surprisal = float(line_tuple[4])
        if line_tuple[6] == "True":
            is_grammatical = True
        else:
            is_grammatical = False

        if is_grammatical:
            if sentpos == 0:    # clear array, reset variables
                if prev_grammatical:
                    print("Error: two consecutive grammatical sentences!")
                    scoredict[case].append(0.)
                    return
                prev_grammatical = True
                if more_probable and grammatical_surp <= ungrammatical_surp:
                    correct += 1.
                total += 1.
                grammatical_surp = 0.
                more_probable = True
            grammatical_sentid = sentid
            grammatical_surp += surprisal

        else:
            if sentpos == 0:
                if not prev_grammatical:
                    if ungrammatical_surp < grammatical_surp:
                        more_probable = False
                prev_grammatical = False
                ungrammatical_surp = surprisal
            else:
                ungrammatical_surp += surprisal
   



assert os.path.isdir(args.score_dir)

if args.case == 'all':
    scoredict = {}
    for filename in os.listdir(args.score_dir):
        if filename.endswith('.wordscores'):
            case = filename.split(".txt")[0]
            with open(os.path.join(args.score_dir, filename), 'r') as wordscores:
                if args.word_compare:
                    do_word_compare(wordscores, scoredict, case)
                else:
                    do_sen_compare(wordscores, scoredict, case)
    for case in scoredict.keys():
        print("{}:\t{} +/- {}".format(case, statistics.mean(scoredict[case]), \
                statistics.pstdev(scoredict[case])))

else:
    scoredict = {}
    for filename in os.listdir(args.score_dir):
        if filename.startswith(args.case) and filename.endswith(".wordscores"):
            with open(os.path.join(args.score_dir, filename), 'r') as wordscores:
                if args.word_compare:
                    do_word_compare(wordscores, scoredict, args.case)
                else:
                    do_sen_compare(wordscores, scoredict, args.case)
    print("{}:\t{} +/- {}".format(args.case, statistics.mean(scoredict[args.case]), \
            statistics.pstdev(scoredict[args.case])))
