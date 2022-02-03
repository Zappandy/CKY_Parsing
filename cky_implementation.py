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

        #for j in range(dims):
        #    if sentence[j-1] in self.flipped_grammar.keys():
        #        self._table[j-1, j] = self.flipped_grammar[sentence[j-1]]
        #    for i in range(j-2, 0, -1):
        #        for k in range(i+1, j-1):
        #            self._table[i, j] ="tito"
        #            if self._table[i, k] and self._table[k, j]:
        #                self._table[i, j] ="tito"
        #                print(k)



        for i in range(1, dims):
            if sentence[i-1] in self.flipped_grammar.keys():
                self._table[i-1, i] = self.flipped_grammar[sentence[i-1]]
                #self._table[i-1, i] = Tree(self.flipped_grammar[sentence[i-1]], list(sentence[i-1]))
                #for symbol in self.flipped_grammar[sentence[i-1]]:
                #    word = Tree(symbol, list(sentence[i-1]))  # pointer 4 rules?
            for j in range(i-2, -1, -1):  # 0 in notes is inclusive
                for k in range(j+1, i+j-(i-2)):  #  3 - 1, 4 - 2
                    if i == 7:
                        if self._table[j, k] and self._table[k, i]:
                            self._table[j, k] + self._table[k, i]
                            self._table[j, i] = self._table[j, k] + self._table[k, i]
        print(self._table)
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
        if type(rhs[0]) is str:
            flipped_grammar.setdefault(rhs[0], set())
            flipped_grammar[rhs[0]].add(rule.lhs())
        else:
            flipped_grammar.setdefault(rhs, set())
            flipped_grammar[rhs].add(rule.lhs())
    return {k: tuple(v) for k, v in flipped_grammar.items()}
    #return flipped_grammar

#https://courses.engr.illinois.edu/cs447/fa2018/Slides/Lecture09.pdf

my_grammar = nltk.data.load("cnf_grammar.cfg")  # nltk.CFG.fromstring

flipped_grammar = get_flipped_grammar(my_grammar)
#x = set(len(testing[k]) for k in testing.keys())

for sent in tokenized_sentences[:1]:
    cky_table = CKYTable(flipped_grammar)
    cky_table.table = sent


#https://www.youtube.com/watch?v=17re2zDBuOM
#https://www.youtube.com/watch?v=VgYa81r_fNA
#https://www.cs.bgu.ac.il/~michaluz/seminar/CKY1.pdf
#https://www.youtube.com/watch?v=MRmVuJ-J3I0&t=4s
