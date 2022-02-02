import nltk
my_grammar = nltk.data.load("grammar.cfg")  # nltk.CFG.fromstring

#TODO: Clean hybrid rules
class CNF:
    def __init__(self, cfg_grammar):
        self.cfg_grammar = cfg_grammar
        self.productions = cfg_grammar.productions()
        # unit
        self.good_non_terminals = []
        self.fake_terminals = []
        # long
        self.long_productions = []
        self.short_productions = []
        self.cnf_counter = 0

    def unitProduction(self):
        for i, prod in enumerate(self.productions):
            non_term_flag = True
            right_side = self.productions[i].rhs()
            for symbol in right_side:
                if isinstance(symbol, str):
                    non_term_flag = False  # reached terminal that should be a str/word
                    break
            if len(right_side) == 1 and non_term_flag:
                self.fake_terminals.append(self.productions[i])
            else:
                self.good_non_terminals.append(self.productions[i])

    def unitRule(self): 
        if bool(self.fake_terminals) is False:
            return nltk.CFG(self.cfg_grammar.start(), self.good_non_terminals)
        fake_term = self.fake_terminals.pop(0)
        for prod in self.productions:
            if prod.lhs() == fake_term.rhs()[0]:
                new_rule = nltk.Production(fake_term.lhs(), prod.rhs())
                if isinstance(new_rule.rhs()[0], str) or len(new_rule) > 1:
                    self.good_non_terminals.append(new_rule)
                else:
                    self.fake_terminals.append(new)
        return self.unitRule()

    def longProduction(self):
        for prod in self.productions:
            if len(prod) > 2 and prod.is_nonlexical:
                self.long_productions.append(prod)
            else:
                self.short_productions.append(prod)

    def longRule(self): 
        if bool(self.long_productions) is False:
            return nltk.CFG(self.cfg_grammar.start(), self.short_productions)
        long_prod = self.long_productions.pop(0)
        new_rhs = []
        inverse_range = len(long_prod.rhs()) - 1
        for idx in range(inverse_range, -1, -2):
            if idx - 2 > -2:
                new_non = [long_prod.rhs()[idx-1], long_prod.rhs()[idx]]
                non_term_head = f"_X{self.cnf_counter}_"
                x_rule = nltk.Production(nltk.Nonterminal(non_term_head), new_non)
                self.short_productions.append(x_rule)
                new_rhs.insert(0, nltk.Nonterminal(non_term_head))
                self.cnf_counter += 1
            else:
                new_rhs.insert(0, long_prod.rhs()[idx])

        # tying new productions
        new_prod = nltk.Production(long_prod.lhs(), tuple(new_rhs))
        if len(new_prod) > 2:
            self.long_productions.append(new_prod)
        else:
            self.short_productions.append(new_prod)
        return self.longRule()

    @classmethod
    def cnfGrammar(cls, grammar):
        unit_cleaner = cls(grammar)
        unit_cleaner.unitProduction()
        new_grammar = unit_cleaner.unitRule()
        long_cleaner = cls(new_grammar)
        long_cleaner.longProduction()
        return long_cleaner.longRule()



cnf_grammar = CNF.cnfGrammar(my_grammar)
with open("cnf_grammar.cfg", 'w') as file:
    cnf_grammar = CNF.cnfGrammar(my_grammar)
    for prod in cnf_grammar.productions():
        file.write(str(prod) + '\n')
    file.close()

#cnf_grammar = nltk.data.load("cnf_grammar.cfg")  # errors because there's non-terminals
#print(cnf_grammar.is_chomsky_normal_form())

#cnf_grammar = nltk.data.load("tito.cfg")
print(cnf_grammar.is_chomsky_normal_form())
print(cnf_grammar.is_binarised())
