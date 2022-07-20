import nltk
import numpy as np
from nltk.grammar import Nonterminal
from nltk.tree import Tree
from collections import OrderedDict
# https://parser.kitaev.io/
class Node:  # for recursive trees
    def __init__(self, rules, left=None, right=None, terminal=None):
        """
        Constructor with rules as left side of grammar rules and 2 nodes as its 2 rules on
        the right side. Terminal indicates whether the word/string is on the right side of 
        the rule. If it is, then this would be the end of the tree.
        """
        self.rules = rules
        self.root = None
        self.endToken = True if terminal else False
        self.non_term_1 = left
        self.non_term_2 = right  # remain as None if non_term_1 is a terminal

class CKYTable:
    def __init__(self, grammar):
        """
        Constructor initialized with grammar to find terminals and 
        2 data structures, plus the root of the tree.
        """
        self.grammar = grammar
        self.terminals = self.terminalsGetter(grammar)
        self._table = None  # explicit rules
        self.backtrack = None  # stored in tree nodes
        self.root = None
        self.backtrack_lis = OrderedDict()

    @property  # getter
    def table(self):
        return self._table

    @table.setter  
    def table(self, sentence):
        """
        sentence: tokenized sentence to be analyzed and broken down by
        the cky in this setter method.
        This method also sets the backtrack nested list and the root of the tree.
        The backtracking table can be tinkered as a linked list
        """
        dims = len(sentence) + 1
        self._table = np.array([[set() for j in range(dims)] for i in range(dims)])
        self.backtrack = np.array([[set() for j in range(dims)] for i in range(dims)])
        

        for i in range(1, dims):
            if sentence[i-1] in self.terminals.keys():
                self._table[i-1, i] = self.terminals[sentence[i-1]]
                self.backtrack[i-1, i].add(Node(rules=self.terminals[sentence[i-1]], terminal=sentence[i-1]))
            for j in range(i-2, -1, -1):  # 0 in notes is inclusive
                #for k in range(j+1, j, -1):  #  works as CKY is supposed to be computed
                #j - 1, j + 1 if j, k == j - 1, k and if rules are correct
                for k in range(j+1, i):  # This loop fills in the last cell, but this 
                    # does not index the correct cells 
                    #print(f"{j} {k} to fill {j}, {i} with {k} {i}")  showing how first loop is right
                    if self._table[j, k] and self._table[k, i]:
                        for left in self._table[j, k]:
                            productions = self.grammar.productions(rhs=left)
                            for prod in productions:
                                if prod.rhs()[1] in self._table[k, i]:
                                    self._table[j, i].add(prod.lhs())
                                    #print(prod.rhs()[0], j, k)  # j k
                                    #print(prod.rhs()[1], k, i)  # k i
                                    self.backtrack_lis[prod.lhs()] = [prod.rhs()[0], prod.rhs()[1]]
                                # backtracking
                                    
                                    #print(f"{j} {k} to fill {j}, {i} with {k} {i}")
                                    # more thorough backtracking
                                    for B in self.backtrack[j, k]:
                                         for C in self.backtrack[k, i]:
                                             if type(B.rules) is set and type(C.rules) is set:
                                                 if prod.rhs()[0] in B.rules and prod.rhs()[1] in C.rules:
                                                     self.backtrack[j, i].add(Node(rules=prod.lhs(), left=prod.rhs()[0], right=prod.rhs()[1]))
                                                     #print(self.backtrack[j, i])
                                                     #print(self.backtrack[j, i].non_term_1)
                                             else:
                                                 if prod.rhs()[0] == B.rules and prod.rhs()[1] == C.rules:
                                                     self.backtrack[j, i].add(Node(rules=prod.lhs(), left=prod.rhs()[0], right=prod.rhs()[1]))

        self.root = self.backtrack[0, -1]
        
        indexes = np.where(self._table == set())
        indexes = np.column_stack((indexes[0], indexes[1]))
        for i in indexes:
            self._table[tuple(i)] = ''  # cleaning up empty sets for empty strings to 
            # better visualize table
        # https://ychai.uk/notes/ blog used as a source for backtracking
           


    def sentenceChecker(self, sentence):
        """
        sentence: Tokenized sentence to review if it is in the grammar
        returns: boolean depending on whether the sentence is in the grammar
        """
        col = len(sentence)
        if self.grammar.start() in self.table[0, col] and len(self.table[0]) == col+1:
             print("Sentence is in the grammar")
             return True
        print("Sentence is not in the grammar")
        return False

    def terminalsGetter(self, grammar):
        """
        grammar: to find terminls and store them in a dictionary to speed up indexing
        returns dictionary with terminals. 
        Notes: structure based on Jane Willborn's CKY implementation
        """
        rules = grammar.productions()
        words = {}
        for rule in rules:
            rhs = rule.rhs()
            if type(rhs[0]) is str:
                words.setdefault(rhs[0], set())
                words[rhs[0]].add(rule.lhs())
        return words



#https://medium.com/@jeffysam02
#https://medium.com/@jeffysam02/introduction-to-matplotlib-part-1-8e3848d1c36?source=user_profile---------15-------------------------------
