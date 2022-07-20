import nltk
from nltk import  treetransforms
from copy import deepcopy
from cky_implementation import *
# https://parser.kitaev.io/
my_grammar = nltk.data.load("grammar.cfg")  # nltk.CFG.fromstring
#print(my_grammar)  #to viz
with open("sentences.txt") as file:
    sentences = file.readlines()
    tokenized_sentences = [nltk.word_tokenize(sent) for sent in sentences]
    file.close()

earley_parser = nltk.parse.EarleyChartParser(my_grammar) 
parsed_sentences = [tuple(earley_parser.parse(sent)) for sent in tokenized_sentences]
bad_indexes = [i for i, tree in enumerate(parsed_sentences) if not bool(tree)]
parsed_sentences = [tree for tree in parsed_sentences if bool(tree)]
good_indexes = tuple(filter(lambda i: i not in bad_indexes, list(range(len(tokenized_sentences)))))
tokenized_sentences = [tokenized_sentences[i] for i in good_indexes]
all_parses = []
for i, sent in enumerate(parsed_sentences):  # 8, 13 and 14 changed to S to run. 9 changed but not running
    parse_count = 0
    for tree in sent:
        print(tree)
        parse_count += 1
    all_parses.append(parse_count)
    print(parse_count)
    print("-------------------------------------")
print(sum(all_parses) / len(parsed_sentences))


my_grammar = nltk.data.load("grammar_cnf.cfg")  # nltk.CFG.fromstring
my_grammar = nltk.data.load("my_cnf_grammar_cnf.cfg")  # nltk.CFG.fromstring
#for i, sent in enumerate(tokenized_sentences):  # 2?
for i, sent in enumerate(tokenized_sentences[:2]):  # 2?
    cky_table = CKYTable(my_grammar)
    cky_table.table = sent
    print(f"{i+1}. {sent}")
    cky_table.sentenceChecker(sent)
    #cky_table.sentenceChecker("muscles are key for movement .".split())  # testing that sentences are not in the grammar
    print(cky_table.backtrack_lis)
    print()

