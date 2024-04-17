       
class Sam:
    def __init__(self, line: str):
        self.data = line.split('\t')
        self.index = self.data[0]
        self.true = self.data[1]
        self.lemma = self.data [2]

class Shire:

    def __init__(self, text: str):

        self.sentences = []
        current_element = []
        for line in text.split("\n"):
            if line == '':
                self.sentences.append(current_element)
                current_element = []
            else:
                current_element.append(Sam(line))
