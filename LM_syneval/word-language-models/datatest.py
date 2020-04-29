import os
from io import open
import torch
import dill

class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    def __init__(self, path, save_to):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(path, 'train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'valid.txt'))
        self.test = self.tokenize(os.path.join(path, 'test.txt'))
        self.save_to = self.save_dict(save_to)

    def save_dict(self, path):
        torch.save(self.dictionary, f, pickle_module=dill)

    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)
        # Add words to the dictionary
        with open(path, 'r', encoding="utf8") as f:
            for line in f:
                words = line.split() + ['<eos>']
                for word in words:
                    self.dictionary.add_word(word)

        # Tokenize file content
        with open(path, 'r', encoding="utf8") as f:
            idss = []
            for line in f:
                words = line.split() + ['<eos>']
                ids = []
                for word in words:
                    ids.append(self.dictionary.word2idx[word])
                idss.append(torch.tensor(ids).type(torch.int64))
            ids = torch.cat(idss)

        return ids

class TestCorpus(object):
    def __init__(self, path, testfname, save_to):
        #self.dictionary = Dictionary()
        self.dictionary = self.load_dict(save_to)
        self.test = self.tokenize(os.path.join(path, testfname))
        self.test_lm = self.sent_tokenize_with_unks(os.path.join(path, testfname))

    def load_dict(self, path):
        with open(path, 'rb') as f:
            fdata = torch.load(f, pickle_module=dill)
            if type(fdata) == type(()):
                return(fdata[3])
            return(fdata)

    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)
        # Add words to the dictionary
        with open(path, 'r', encoding="utf8") as f:
            for line in f:
                words = ['<eos>'] + line.split()
                for word in words:
                    self.dictionary.add_word(word)

        # Tokenize file content
        with open(path, 'r', encoding="utf8") as f:
            idss = []
            for line in f:
                words = ['<eos>'] + line.split()
                ids = []
                for word in words:
                    ids.append(self.dictionary.word2idx[word])
                idss.append(torch.tensor(ids).type(torch.int64))
            ids = torch.cat(idss)

        return ids
        
    def sent_tokenize_with_unks(self, path):
        assert os.path.exists(path)
        all_ids = []
        sents = []
        grammatical = []
        with open(path, 'r') as f:
            for line in f:
                is_grammatical = line.split('\t')[0].strip()
                grammatical.append(is_grammatical)
                sentence = line.split('\t')[1].strip()
                sents.append(sentence)
                words = ['<eos>'] + sentence.split()
                n_tokens = len(words)
                
                ids = torch.LongTensor(n_tokens)
                token = 0
                for word in words:
                    if word not in self.dictionary.word2idx:
                        ids[token] = self.dictionary.add_word("<unk>")
                    else:
                        ids[token] = self.dictionary.word2idx[word]
                    token += 1
                all_ids.append(ids)
            return (sents, all_ids, grammatical)
