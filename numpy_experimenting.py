#import numpy as np
#lemmas = []
#contexts = []

#lemma_to_index = {lemma: i for i, lemma in enumerate(lemmas)}
#context_to_index = {context: i for i, context in enumerate(contexts)}

#NxC = np.zeros((len(lemmas), len(contexts)))

#for lemma, context in [('lemma1', 'context1'), ('lemma2', 'context2'), ('lemma3', 'context3')]:
 #   NxC[lemma_to_index[lemma], context_to_index[context]] = 1

#print(NxC)

'''
We start by importing Sam, who'll carry all the important stuff ! Sam.index gives the index in the sentence, Sam.lemma gives the lemma...
'''
       
class Sam:
    def __init__(self, line: str):
        if '\t' in line :
            self.data = line.split('\t')
            self.index = self.data[0]
            self.true = self.data[1]
            self.lemma = self.data [2]
        else : 
            self.lemma = line    
        

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
import numpy as np

def andmyBOW(sentence: list, fellowship: dict, the_ring: set, bow= 2):
    
    for idx, cur_word in enumerate(sentence):
        if (cur_word.lemma != "<d>") and (cur_word.lemma != "<f>"):
            fellowship.setdefault(cur_word.lemma, dict())

            prev_idx = 1
            post_idx = 1

            while prev_idx <= bow:
                context = (f"-{prev_idx}", sentence[idx - prev_idx].lemma)
                the_ring.add(context)
                fellowship[cur_word.lemma][context] = fellowship[cur_word.lemma].get(context, 0) + 1
                prev_idx += 1 

            while post_idx <= bow:
                context = (f"+{post_idx}", sentence[idx + post_idx].lemma)
                the_ring.add(context)
                fellowship[cur_word.lemma][context] = fellowship[cur_word.lemma].get(context, 0) + 1
                post_idx += 1

    return fellowship, the_ring

def isildursHeir(fellowship, the_ring):
    context_to_index = {context: i for i, context in enumerate(sorted(the_ring))}

    ofTheKing = np.zeros((len(fellowship), len(the_ring)))

    for i, (word, context_dict) in enumerate(fellowship.items()):
        for context, count in sorted(context_dict.items()):
            j = context_to_index[context]
            ofTheKing[i, j] = count

    return ofTheKing


with open('/Users/atillaarslan/projettal/estrepublicain.extrait-aa.19998.outmalt', "r") as conllu:
    text = Shire(conllu.read())


fellowship = dict()
the_ring = set()

for sentence in text.sentences:
    andmyBOW(sentence, fellowship, the_ring, bow= 2)

ofTheKing = isildursHeir(fellowship, the_ring)
print(ofTheKing.shape)
print(ofTheKing[:40, :])
