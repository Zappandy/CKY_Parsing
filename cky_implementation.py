import nltk
from parser import *
import numpy as np
from nltk.grammar import Nonterminal
from nltk.tree import Tree
# https://parser.kitaev.io/
class Node:  # for recursive trees
    def __init__(self, rules, terminal):
        #self.symbol = symbol
        self.rules = rules
        self.root = None
        self.endToken = True
        #self.non_term_1 = non_term_1
        #self.non_term_2 = non_term_2  # remain as None if non_term_1 is a terminal

    #def __repr__(self):
    #    return self.rules
class CKYTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.flipped_grammar = self.get_flipped_grammar(grammar)
        self._table = None

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, sentence):
        dims = len(sentence) + 1
        self._table = np.empty((dims, dims), dtype=object)

        indexes = np.where(self._table == None)
        indexes = np.column_stack((indexes[0], indexes[1]))
        for i in indexes:
            self._table[tuple(i)] = set()

        #for i in range(1, dims):
        #    if sentence[i-1] in self.flipped_grammar.keys():
        #        #self._table[i-1, i] = Node(self.flipped_grammar[sentence[i-1]])
        #        self._table[i-1, i] = self.flipped_grammar[sentence[i-1]]
        #for i in range(2, dims):
        #    for j in range(dims-i):  # 0 in notes is inclusive
        #        for k in range(1, i):
                    #left = self._table[j, j+k]
                    #right = self._table[j+k, j+i]

                    #for l_rule in left:
                    #    productions = self.grammar.productions(rhs=l_rule)
                    #    for prod in productions:
                    #        if prod.rhs()[1] in right:
                    #            print(prod.lhs())
                    #            self._table[j, j+i].add(prod.lhs()) 

                            #for 
        #print(self._table)


        for i in range(1, dims):
            if sentence[i-1] in self.flipped_grammar.keys():
                #self._table[i-1, i] = Node(self.flipped_grammar[sentence[i-1]])
                self._table[i-1, i] = self.flipped_grammar[sentence[i-1]]
            for j in range(i-2, -1, -1):  # 0 in notes is inclusive
                #for k in range(j+1, j, -1):  #  works as CKY is supposed to be computed
                #j - 1, j + 1 if j, k == j - 1, k and if rules are correct
                for k in range(j+1, i+1):  # This loop fills in the last cell
                    if self._table[j, k] and self._table[k, i]:
                        for left in self._table[j, k]:
                            productions = self.grammar.productions(rhs=left)
                            for prod in productions:
                                if prod.rhs()[1] in self._table[k, i]:
                                    self._table[j, i].add(prod.lhs())
        print(self._table)
        raise SystemExit

                        #cells = [self._table[j, k].rules, self._table[k, i].rules]
                        #permutations = [(left, right) for left in cells[0] for right in cells[1]]
                        #for per in permutations:
                        #    if per in self.flipped_grammar.keys():
                        #        self._table[j, i] = Node(self.flipped_grammar[per])
                    #print([j, k, f"cell to fill in {j}, {i}", k, i])  # to show first loop is the right one
                    # shows how weird the rules are with the "right" loop


    def sentenceChecker(self, sentence):
        col = len(sentence)
        print(self.grammar.start())  # _start
        if self.table[0, col]:
            print(self.table[0, col].rules)  # _start
            if self.grammar.start() in self.table[0, col].rules:
                print("Sentence is in the grammar")
                return True
        print("Sentence is not in the grammar")
        return False

    def get_flipped_grammar(self, grammar):
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
        return flipped_grammar

    def prettyTable(self):
        indexes = np.where(self._table != None)
        indexes = np.column_stack((indexes[0], indexes[1]))
        for i in indexes:
            self._table[tuple(i)] = self._table[tuple(i)].rules

    #def __str__(self):
    #    self.prettyTable()
    #    return f"{self._table}"

    #def __repr__(self):
        #sentence = np.array(sentence)
        #self._table = np.vstack((sentence, self._table[:-1, 1:]))
        #return self._table[:-1, 1:]

#https://courses.engr.illinois.edu/cs447/fa2018/Slides/Lecture09.pdf

#https://github.com/SouravDutta91/CKY-Recognizer-Parser/blob/master/cky.ipynb
#https://medium.com/@jeffysam02
#https://medium.com/@jeffysam02/introduction-to-matplotlib-part-1-8e3848d1c36?source=user_profile---------15-------------------------------
my_grammar = nltk.data.load("grammar_cnf.cfg")  # nltk.CFG.fromstring
#my_grammar = nltk.data.load("ber_grammar-cnf.cfg")  # nltk.CFG.fromstring
#my_grammar = nltk.data.load("my_cnf_grammar.cfg")  
for i, sent in enumerate(tokenized_sentences[5:6]):  # 2?
    cky_table = CKYTable(my_grammar)
    print(sent)
    cky_table.table = sent
    print()
    print(f"{i+1}. {sent}")
    cky_table.sentenceChecker(sent)
    cky_table.sentenceChecker("jiji eats tito".split())
    cky_table.prettyTable()
    print(cky_table.table)
    print()

#https://www.youtube.com/watch?v=17re2zDBuOM
#https://www.youtube.com/watch?v=VgYa81r_fNA
#https://www.cs.bgu.ac.il/~michaluz/seminar/CKY1.pdf
#https://www.youtube.com/watch?v=MRmVuJ-J3I0&t=4s
