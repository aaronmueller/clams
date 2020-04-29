import os

with open('forbert.tsv', 'w') as outfile:
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            case = filename.split('.txt')[0]
            with open(filename, 'r') as infile:
                g = ""
                ug = ""
                for line in infile:
                    line_tuple = line.strip().split('\t')
                    if line_tuple[0] == "True":
                        is_grammatical = True
                    else:
                        is_grammatical = False
                    sentence = line_tuple[1]

                    if is_grammatical:
                        g = sentence
                    else:
                        ug = sentence
                        outfile.write(case+'\t'+'de'+'\t'+g+'\t'+ug+'\n')
