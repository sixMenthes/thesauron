       
class Token:
    def __init__(self, line: str):
        if '\t' in line :
            self.data = line.split('\t')
            self.index = self.data[0]
            self.true = self.data[1]
            self.lemma = self.data [2]
            self.cat = self.data [3]
        else : 
            self.lemma = line
            self.cat = 'undefined'

    def __eq__(self, other):
        if isinstance(other, Token):
            return ((self.lemma == other.lemma) and (self.cat == other.cat))
        return False

    def __hash__(self):
        return hash((self.lemma, self.cat))   