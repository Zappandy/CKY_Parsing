import nltk
from parser import *
import numpy as np
from nltk.grammar import Nonterminal
from nltk.tree import Tree
# https://parser.kitaev.io/
class CKYTable:
    def __init__(self, flip_grammar):
        self.flipped_grammar = flip_grammar
        self._table = None

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, sentence):
        dims = len(sentence) + 1
        self._table = np.empty((dims, dims), dtype=object)
        fake_table = np.empty((dims, dims), dtype=object)

        for i in range(1, dims):
            if sentence[i-1] in self.flipped_grammar.keys():
                self._table[i-1, i] = self.flipped_grammar[sentence[i-1]]
                #self._table[i-1, i] = Tree(self.flipped_grammar[sentence[i-1]], list(sentence[i-1]))
                #for symbol in self.flipped_grammar[sentence[i-1]]:
                #    word = Tree(symbol, list(sentence[i-1]))  # pointer 4 rules?
            for j in range(i-2, -1, -1):  # 0 in notes is inclusive
                for k in range(j+1, i+j-(i-2)):  #  3 - 1, 4 - 2
                    if i == 2:
                        if self._table[j, k] and self._table[k, i]:
                            print(self._table[j, k])
                            print(self._table[k, i])
                            rules = [self._table[j, k], self._table[k, i]]
                            permutations = [(x, y) for x in rules[0] for y in rules[1]]
                            print(permutations)
                            for per in permutations:
                                continue



                            #lengths = OrderedDict()
                            #lengths = {tuple(self._table[j, k]): len(self._table[j, k]), tuple(self._table[k, i]): len(self._table[k, i])}
                            #values = tuple(set(lengths.values()))
                            #print(lengths)
                            #print(values)
                            #if len(values) > 1:
                            #    cycle_rule = rules[0] if values[0] > values[1] else rules[1]
                            #    non_cycle_rule = rules[0] if values[0] < values[1] else rules[1]
                            #    print(cycle_rule)
                            #    print(non_cycle_rule)
                            #    raise SystemExit
                            #else:
                            #    self._table[j, i], *_ = zip(self._table[j, k], self._table[k, i])  # buffer value
        print(self._table)
        raise SystemExit
        #non_terms = [rule for rule in self.flipped_grammar.keys() if type(rule) is not str]
        #sentence = np.array(sentence)
        #self._table = np.vstack((sentence, self._table[:-1, 1:]))

            #for prod in my_grammar.productions():
            #    if sentence[i-1] == prod.rhs()[0]:
            #        if not bool(fake_table[i-1, i]):
            #            fake_table[i-1, i] = {prod.lhs()}
            #        else:
            #            fake_table[i-1, i].add(prod.lhs())


def get_flipped_grammar(grammar):
    rules = grammar.productions()
    flipped_grammar = {}
    for rule in rules:
        rhs = rule.rhs()
        if type(rhs[0]) is str:  # careful with sets because of different iterations
            flipped_grammar.setdefault(rhs[0], set())
            flipped_grammar[rhs[0]].add(rule.lhs())
        else:
            flipped_grammar.setdefault(rhs, set())
            flipped_grammar[rhs].add(rule.lhs())
    #return {k: tuple(v) for k, v in flipped_grammar.items()}
    return flipped_grammar

#https://courses.engr.illinois.edu/cs447/fa2018/Slides/Lecture09.pdf

#https://github.com/SouravDutta91/CKY-Recognizer-Parser/blob/master/cky.ipynb
#https://medium.com/@jeffysam02
#https://medium.com/@jeffysam02/introduction-to-matplotlib-part-1-8e3848d1c36?source=user_profile---------15-------------------------------
my_grammar = nltk.data.load("cnf_grammar.cfg")  # nltk.CFG.fromstring
flipped_grammar = get_flipped_grammar(my_grammar)
for tup in flipped_grammar.keys():
    if type(tup) is not str:
        for i in tup:
            if i.symbol() == 'VBZ':
                print(tup)
                print(flipped_grammar[tup])
                #raise SystemExit
print()
for sent in tokenized_sentences[:1]:
    cky_table = CKYTable(flipped_grammar)
    cky_table.table = sent


#https://www.youtube.com/watch?v=17re2zDBuOM
#https://www.youtube.com/watch?v=VgYa81r_fNA
#https://www.cs.bgu.ac.il/~michaluz/seminar/CKY1.pdf
#https://www.youtube.com/watch?v=MRmVuJ-J3I0&t=4s
