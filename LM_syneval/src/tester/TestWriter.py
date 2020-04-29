import logging
import pickle
import random
import os
logging.basicConfig(level=logging.INFO)

class TestWriter():
    def __init__(self, template_dir, sent_file, max_num=None):
        self.name_lengths = {}
        self.key_lengths = {}
        self.template_dir = template_dir
        self.out_file = os.path.join(self.template_dir, sent_file)
        self.max_num = max_num

    def write_tests(self, all_sents, unit_type):
        logging.info("Writing tests...")
        with open(self.out_file, 'w') as f:
            name_length = 0
            key_length = 0
            for name in all_sents.keys():
                if "npi" in name:
                    multiplier=3
                else: multiplier=2
                self.key_lengths[name] = {}
                for key in all_sents[name].keys():
                    sents = all_sents[name][key]
                    if self.max_num:
                        random.shuffle(sents)
                        sents = sents[:self.max_num]
                    key_length += multiplier * len(sents)
                    self.key_lengths[name][key] = key_length
                    name_length += multiplier * len(sents)
                    for sent in sents:
                        for i in range(len(sent)):
                            if unit_type != 'word':
                                chars = [x if x != ' ' else '/s' for x in sent[i]+' ']
                                f.write(' '.join(chars)+' . /s \n')
                            else:
                                f.write(sent[i] + " . \n")
                    self.name_lengths[name] = name_length
        pickle.dump((self.key_lengths,self.name_lengths),\
                    open(os.path.join(self.template_dir,'writer_data.pkl'),'wb'))

    def read_tests(self):
        logging.info("Reading tests...")
        self.key_lengths,self.name_lengths =\
            pickle.load(open(os.path.join(self.template_dir,'writer_data.pkl'),'rb'))

