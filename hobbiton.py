       
class Sam:
    def __init__(self, line: str):
        if '\t' in line :
            self.data = line.split('\t')
            self.index = self.data[0]
            self.true = self.data[1]
            self.lemma = self.data [2]
            self.category = self.data [3]
        else : 
            self.lemma = line
            self.category = 'undef'    
        

class Shire:

    def __init__(self, text: str):

        self.sentences = []
        current_element = []
        for line in text.split("\n"):
            if line == '':
                current_element.insert(0,Sam("<d>"))
                current_element.insert(1, Sam("<d>"))
                current_element.append(Sam("<f>"))
                current_element.append(Sam("<f>"))
                self.sentences.append(current_element)
                current_element = []
            else:
                current_element.append(Sam(line))
