"""This class has proven itself really useful. It reads 1 line (i.e. 1 word) of the conllu file, splits it on tabulation and defines a Token as a tuple lemma - pos tag. 
We also had to define the __eq__ function to compare both of these elements, and the __hash__ function subsequently."""

class Token:
    def __init__(self, line: str):
        if '\t' in line :
            self.data = line.split('\t')
            self.lemma = self.data [2]
            self.cat = self.data [3]
        else : 
            self.lemma = line
            self.cat = 'undef'

    def __eq__(self, other):
        if isinstance(other, Token):
            return ((self.lemma == other.lemma) and (self.cat == other.cat))
        return False

    def __hash__(self):
        return hash((self.lemma, self.cat))

    def init_for_search(self, lemma: str, category: str): #this part is useful for the finding the actual synonyms, since we'll need to input a word and a category. 
        #We will then tokenize them so as to compare it to the objects previously stored.
        self.lemma = lemma
        self.cat = category
    
