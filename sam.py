
def extractLemma(line:str):
    return line.split('\t')[2]



class Sam:
    def __init__(self, lemma, sentence_index):
        self.lemma = lemma
        self.sentence_index = sentence_index

    def __str__(self):
        return f"Lemma: {self.lemma}, Sentence Index: {self.sentence_index}"

    def __repr__(self):
        return str(self)
def conllu_reader(path: str) -> list:
    with open(path, "r") as conllu:
        post_text = []
        sentence_index = 0
        sentence = []
        for token in conllu.readlines():
            token = token.strip()
            if token:
                sentence.append(Sam(extractLemma(token), sentence_index))
            else:
                if sentence:
                    post_text.extend(sentence)
                    post_text.append('')
                    sentence = []
                    sentence_index += 1
        if sentence:
            post_text.extend(sentence)
    return post_text

conllu_reader('/Users/atillaarslan/projettal/estrepublicain.extrait-aa.19998.outmalt')
