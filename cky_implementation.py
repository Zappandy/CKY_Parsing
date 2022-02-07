import nltk
from parser import *
import numpy as np
from nltk.grammar import Nonterminal
from nltk.tree import Tree
from collections import OrderedDict
# https://parser.kitaev.io/
class Node:  # for recursive trees
    def __init__(self, rules, left=None, right=None, terminal=None):
        #self.symbol = symbol
        self.rules = rules
        self.root = None
        self.endToken = True if terminal else False
        self.non_term_1 = left
        self.non_term_2 = right  # remain as None if non_term_1 is a terminal
        self.nodes_backtrack = OrderedDict()

    #def __repr__(self):
    #    return self.rules
class CKYTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.terminals = self.terminalsGetter(grammar)
        self._table = None
        self.backtrack = None
        self.root = None

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, sentence):
        dims = len(sentence) + 1
        self._table = np.array([[set() for j in range(dims)] for i in range(dims)])
        self.backtrack = [[list() for j in range(dims)] for i in range(dims)]
        

        for i in range(1, dims):
            if sentence[i-1] in self.terminals.keys():
                self._table[i-1, i] = self.terminals[sentence[i-1]]
                self.backtrack[i-1][i].append(Node(rules=self.terminals[sentence[i-1]], terminal=sentence[i-1]))
            for j in range(i-2, -1, -1):  # 0 in notes is inclusive
                #for k in range(j+1, j, -1):  #  works as CKY is supposed to be computed
                #j - 1, j + 1 if j, k == j - 1, k and if rules are correct
                for k in range(j+1, i):  # This loop fills in the last cell
                    #print(f"{j} {k} to fill {j}, {i} with {k} {i}")  showing how first loop is right
                    if self._table[j, k] and self._table[k, i]:
                        for left in self._table[j, k]:
                            productions = self.grammar.productions(rhs=left)
                            for prod in productions:
                                if prod.rhs()[1] in self._table[k, i]:
                                    self._table[j, i].add(prod.lhs())
                                    print(prod.rhs()[0], j, k)
                                    print(prod.rhs()[1], k, i)
                                    print(prod.lhs())
                                    print()
                                # backtracking
                                    #print(f"{j} {k} to fill {j}, {i} with {k} {i}")
                                    #print(self._table[0, 2], self._table[1, 3], self._table[0, 3])
                                    for B in self.backtrack[j][k]:
                                         for C in self.backtrack[k][i]:
                                             if type(B.rules) is set and type(C.rules) is set:
                                                 if prod.rhs()[0] in B.rules and prod.rhs()[1] in C.rules:
                                                     self.backtrack[j][i].append(Node(rules=prod.lhs(), left=prod.rhs()[0], right=prod.rhs()[1]))
                                             else:
                                                 if prod.rhs()[0] == B.rules and prod.rhs()[1] == C.rules:
                                                     self.backtrack[j][i].append(Node(rules=prod.lhs(), left=prod.rhs()[0], right=prod.rhs()[1]))

        self.root = self.backtrack[0][-1]
        
        indexes = np.where(self._table == set())
        indexes = np.column_stack((indexes[0], indexes[1]))
        for i in indexes:
            self._table[tuple(i)] = ''
        #print(self._table)
        #print(self.root)
        # https://ychai.uk/notes/
        #print(self.backtrack)
           


    def sentenceChecker(self, sentence):
        col = len(sentence)
        if self.grammar.start() in self.table[0, col] and len(self.table[0]) == col+1:
             print("Sentence is in the grammar")
             return True
        print("Sentence is not in the grammar")
        return False

    def terminalsGetter(self, grammar):
        rules = grammar.productions()
        words = {}
        for rule in rules:
            rhs = rule.rhs()
            if type(rhs[0]) is str:
                words.setdefault(rhs[0], set())
                words[rhs[0]].add(rule.lhs())
        return words



#https://courses.engr.illinois.edu/cs447/fa2018/Slides/Lecture09.pdf

#https://github.com/SouravDutta91/CKY-Recognizer-Parser/blob/master/cky.ipynb
#https://medium.com/@jeffysam02
#https://medium.com/@jeffysam02/introduction-to-matplotlib-part-1-8e3848d1c36?source=user_profile---------15-------------------------------
my_grammar = nltk.data.load("grammar_cnf.cfg")  # nltk.CFG.fromstring
for i, sent in enumerate(tokenized_sentences[0:1]):  # 2?
    cky_table = CKYTable(my_grammar)
    print(sent)
    cky_table.table = sent
    print()
    print(f"{i+1}. {sent}")
    cky_table.sentenceChecker(sent)
    cky_table.sentenceChecker("muscles are key for movement .".split())
    print()

#https://www.youtube.com/watch?v=17re2zDBuOM
#https://www.youtube.com/watch?v=VgYa81r_fNA
#https://www.cs.bgu.ac.il/~michaluz/seminar/CKY1.pdf
#https://www.youtube.com/watch?v=MRmVuJ-J3I0&t=4s
