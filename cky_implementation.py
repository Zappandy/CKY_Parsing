import nltk
from parser import *
import numpy as np
from nltk.grammar import Nonterminal
from nltk.tree import Tree
# https://parser.kitaev.io/
class CKYTable:
    def __init__(self, flip_grammar, words):
        self.flipped_grammar = flip_grammar
        self.words = words
        self._table = None

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, sentence):
        dims = len(sentence) + 1
        self._table = np.empty((dims, dims), dtype=object)
        for i in range(1, dims):
            if sentence[i-1] in self.words:
                for symbol in self.flipped_grammar[(sentence[i-1],)]:
                    word = Tree(symbol, list(sentence[i-1]))
                    self._table[i-1, i] = word

def get_flipped_grammar(grammar):
    rules = grammar.productions()
    flipped_grammar = {}
    for rule in rules:
        rhs = rule.rhs()
        if rhs not in flipped_grammar:
            flipped_grammar[rhs] = set()
        flipped_grammar[rhs].add(rule.lhs())
    return flipped_grammar


my_grammar = nltk.data.load("cnf_grammar.cfg")  # nltk.CFG.fromstring

flipped_grammar = get_flipped_grammar(my_grammar)
words = [word for right_hand in flipped_grammar.keys() for word in right_hand if type(word) is str] 
#x = set(len(testing[k]) for k in testing.keys())

for sent in tokenized_sentences[:1]:
    cky_table = CKYTable(flipped_grammar, words)
    cky_table.table = sent
    print(cky_table.table)



