import nltk
from nltk import  treetransforms
from copy import deepcopy
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
for i, sent in enumerate(parsed_sentences):  # 8 changed to S to run. 9, 13, and 14 not running
    parse_count = 0
    for tree in sent:
        print(tree)
        parse_count += 1
    all_parses.append(parse_count)
    print(parse_count)
    print("-------------------------------------")
print(sum(all_parses) / len(parsed_sentences))

#https://github.com/mateusmoury/pln-cky/blob/master/pcfg.py
#https://python.hotexamples.com/examples/nltk.treetransforms/-/chomsky_normal_form/python-chomsky_normal_form-function-examples.html
#https://medium.com/swlh/cyk-cky-f63e347cf9b4
#https://github.com/dj1121/nltk_parsing


#https://www.javatpoint.com/automata-chomskys-normal-form
