import os
from collections import deque
from collections import defaultdict

class Grammar:
    def __init__(self, args):
        self.nonterminals = set()
        self.vary = set()  # set of Nonterminals
        self.start = Nonterminal(name="S")
        self.rules = defaultdict(lambda: deque())
        self.args = args
        self.vocab = set()
        if self.args.check_vocab is not None:
            self.init_vocab()
   
    def init_vocab(self):
        if os.path.isfile(self.args.check_vocab):
            with open(self.args.check_vocab, "r") as vocab_file:
                for line in vocab_file:
                    token = line.strip()
                    self.vocab.add(token)
        else:
            raise Exception("Not a valid vocab file: {}".format(self.args.check_vocab))

    # read grammar rule from line
    def add_rules(self, lhs, rhs_string):
        for option in rhs_string.split("|"):
            rhs = []
            outstring = option.strip()
            for token in outstring.split(" "):
                if "[" in token: # is a nonterminal
                    token_nt = Nonterminal()
                    token_nt.read_nt(token)
                    # self.nonterminals.add(token_nt)
                    rhs.append(token_nt)
                else:           # is a terminal
                    rhs.append(token)
                    if self.args.check_vocab is not None:
                        if token not in self.vocab:
                            print("Token not in vocabulary: {}".format(token))
            self.rules[lhs].append(rhs)

    # read grammar from file
    def read(self, infile):
        with open(infile, 'r') as grammar_file:
            for line in grammar_file:
                # if line is empty
                if not line.strip():
                    continue
                # if line is a comment
                if line.strip().startswith("#"):
                    continue
                if line.strip().startswith("vary"):
                    varystring = line.split(":")[1]
                    varies = varystring.split(";")
                    for vary_item in varies:
                        vary_item = vary_item.strip()
                        vary_nt = Nonterminal()
                        vary_nt.read_nt(vary_item)
                        self.vary.add(vary_nt)
                    continue

                lhs = line.split(" ")[0].strip()
                lhs_nonterminal = Nonterminal()
                if "[" in lhs:
                    lhs_nonterminal.read_nt(lhs)
                else:
                    lhs_nonterminal.name = lhs
                self.nonterminals.add(lhs_nonterminal)
                '''
                if "[" in lhs:
                    lhs_name = lhs.split("[")[0].strip()
                    lhs_attributes = lhs.split("[")[1][:-1].split(",")
                    for idx, attribute in enumerate(lhs_attributes):
                        lhs_attributes[idx] = attribute.strip()
                    lhs_nonterminal = Nonterminal(lhs_name, att=lhs_attributes)
                else:
                    lhs_nonterminal = Nonterminal(lhs)
                '''

                rhs = line.split(" ", 1)[1].strip()
                self.add_rules(lhs_nonterminal, rhs)
    
    def nt_generate(self, current_nt):
        # check to see what we can vary
        vary = False
        vary_attributes = set()
        vary_len = 1
        for vary_nt in self.vary:
            if vary_nt.name == current_nt.name:
                vary = True
                vary_attributes.add(frozenset(vary_nt.attributes))

        out_list = []
        if not vary:
            for option in self.rules[current_nt]:
                out_list.append(option)
        else:
            current_att = current_nt.attributes
            # find all relevant NTs
            for att_set in vary_attributes:
                if not att_set:     # any attribute goes
                    # list of lists, each containing a parallel structure to nt's rhs
                    alternate_options = []
                    nt_idx = 0
                    for nt in self.nonterminals:
                        if nt.name == current_nt.name and nt.attributes != current_nt.attributes:
                            alternate_options.append([])
                            for option in self.rules[nt]:
                                alternate_options[nt_idx].append(option)
                            nt_idx += 1

                    for idx, option in enumerate(self.rules[current_nt]):
                        out_list.append(option)
                        for alternate_option in alternate_options:
                            out_list.append(alternate_option[idx])
                    vary_len = len(alternate_options) + 1
                            
                    '''
                    for nt in self.nonterminals:
                        if nt.name == current_nt.name:
                            for option in self.rules[nt]:
                                out_list.append(option)
                    '''
                    break
                # else, we have to see which attributes we can vary
                att_overlap = att_set.intersection(current_nt.attributes)
                if len(att_overlap) == len(att_set):    # we have a match!
                    alternate_options = []
                    nt_idx = 0
                    for nt in self.nonterminals:
                        if nt.name == current_nt.name:
                            this_overlap = nt.attributes.intersection(att_set)
                            if len(this_overlap) == len(att_set):
                                alternate_options.append([])
                                for option in self.rules[nt]:
                                    alternate_options[nt_idx].append(option)
                                nt_idx += 1

                    for idx, option in enumerate(self.rules[current_nt]):
                        out_list.append(option)
                        for alternate_option in alternate_options:
                            out_list.append(alternate_option[idx])
                    vary_len = len(alternate_options) + 1
        
        return (out_list, vary, vary_len)

    # generate all possible sentences using 'vary' system
    def sen_generate(self, evalfile):
        templates = self.rules[self.start]
        original_num_templates = len(templates)
        while templates:
            num_templates = len(templates)
            template = templates.popleft()
            eval_tuples = []   # list of tuples in evaluation set
                               # tuple[0] is string; tuple[1] is grammaticality

            for token in template:
                # if terminal
                if isinstance(token, str):
                    if not eval_tuples:
                        eval_tuples.append((token, True))
                    else:
                        for idx, eval_tuple in enumerate(eval_tuples):
                            string = eval_tuple[0] + " "+token
                            # preserve prior grammaticality values
                            eval_tuples[idx] = (string, eval_tuple[1])
                # if nonterminal
                elif isinstance(token, Nonterminal):
                    possible_strings, vary, vary_len = self.nt_generate(token)
                    if not eval_tuples:
                        for idx, possible_string in enumerate(possible_strings):
                            if idx % vary_len == 0:
                                grammatical = True
                            else:
                                grammatical = False
                            eval_string = ' '.join(possible_string)
                            eval_tuples.append((eval_string, grammatical))
                    else:
                        if vary:
                            new_eval_tuples = []
                            for eval_tuple in eval_tuples:
                                for idx, possible_string in enumerate(possible_strings):
                                    eval_string = eval_tuple[0]
                                    printable_str = ' '.join(possible_string)
                                    new_string = eval_string + " " + printable_str
                                    if idx % vary_len == 0:
                                        grammatical = True
                                    else:
                                        grammatical = False
                                    new_eval_tuples.append((new_string, grammatical))
                            eval_tuples = new_eval_tuples
                        else:
                            new_eval_tuples = []
                            for possible_string in possible_strings:
                                for eval_tuple in eval_tuples:
                                    eval_string = eval_tuple[0]
                                    grammatical = eval_tuple[1]
                                    printable_str = ' '.join(possible_string)
                                    new_string = eval_string + " " + printable_str
                                    new_eval_tuples.append((new_string, grammatical))
                            eval_tuples = new_eval_tuples

            # print all strings to eval file
            write_or_append = 'w' if original_num_templates == num_templates else 'a'
            with open(evalfile, write_or_append) as outfile:
                for idx, eval_tuple in enumerate(eval_tuples):
                    outfile.write(str(eval_tuple[1])+'\t'+eval_tuple[0]+'\n')

class Nonterminal:
    def __init__(self, name="", att=set()):
        self.name = name
        self.attributes = att

    # define __eq__ and __hash__ s.t. Nonterminals with the same
    # name and attributes are treated as equivalent
    def __eq__(self, other):
        if not isinstance(other, Nonterminal):
            return NotImplemented
        return self.name == other.name and self.attributes == other.attributes
    
    def __hash__(self):
        return hash((self.name, frozenset(self.attributes)))

    def read_nt(self, instring):
        nt_name = instring.split("[")[0].strip()
        nt_attributes = instring.split("[")[1][:-1].strip()
        if not nt_attributes:   # if there are no attributes
            self.name = nt_name
            return
        att_list = []
        if "," in nt_attributes: # if there are multiple attributes
            for attribute in nt_attributes.split(","):
                att_list.append(attribute.strip())
        else:
            att_list.append(nt_attributes)
        # convert list of attributes to set
        attribute_set = set(att_list)
        self.name = nt_name
        self.attributes = attribute_set
