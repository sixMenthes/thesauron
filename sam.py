       
class Sam:
    def __init__(self, line: str):
        self.data = line.split('\t')
        self.index = self.data[0]
        self.true = self.data[1]
        self.lemma = self.data [2]
