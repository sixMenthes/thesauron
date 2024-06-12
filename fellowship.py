'''
We start by importing Sam, who'll carry all the important stuff ! Sam.index gives the index in the sentence, Sam.lemma gives the lemma...
'''
from hobbiton import Shire, Sam
import numpy as np

verbs = set()
names = set()
adjectives = set()
adverbs = set()

the_ring = {
    'V': verbs,
    'N': names,
    'A': adjectives,
    'ADV': adverbs
}

'''We're gonna output 4 thesauri : one for verbs, one for names, one for adjectives and one for verbs. 
This function reads a conllu sentence and, for each word (Sam object containing the conllu attributes)'''
def andmyBOW(sentence: list, fellowship: dict, the_ring: dict, bow= 2, lookbehind= True):
    
    for idx, cur_word in enumerate(sentence):
        if cur_word.category in the_ring.keys():
            fellowship.setdefault(cur_word, dict())

            prev_idx = 1
            post_idx = 1

            if lookbehind == True:
                while prev_idx <= bow:
                    context = (f"-{prev_idx}", sentence[idx - prev_idx])
                    the_ring[cur_word.category].add(context)
                    fellowship[cur_word][context] = fellowship[cur_word].get(context, 0) + 1
                    prev_idx += 1 

            while post_idx <= bow:
                context = (f"+{post_idx}", sentence[idx + post_idx])
                the_ring[cur_word.category].add(context)
                fellowship[cur_word][context] = fellowship[cur_word].get(context, 0) + 1
                post_idx += 1

    return fellowship, the_ring

''''''

def minesOfMoria (fellowship: dict, the_ring: dict):
    Aragorn = []
    for word in fellowship.keys():
        word_vec = np.zeros(len(the_ring[word.category]))
        for idx, context in enumerate(the_ring[word.category]):
            if context in fellowship[word].keys():
                word_vec[idx] = fellowship[word][context]
            else:
                word_vec[idx] = 0
        Aragorn.append(word_vec)


# def isildursHeir (fellowship: dict, the_ring: dict):

#     Aragorn = []

#     for word in fellowship.keys():
#         word_vec = np.zeros(len(the_ring))
#         for idx, context in enumerate(the_ring[word.category]):
#             if context in fellowship[word].keys():
#                 word_vec[idx] = fellowship[word][context]
#             else:
#                 word_vec[idx] = 0
#         Aragorn.append(word_vec)
    
#     ofTheKing = np.stack(Aragorn, axis=1)

#     return ofTheKing



with open('/Users/leo/LIL3S2/projet_tal/estrepublicain.extrait-aa.19998.outmalt', "r") as conllu:
    text = Shire(conllu.read())

fellowship = {}

for sentence in text.sentences:
    andmyBOW(sentence, fellowship, the_ring)

print(len(fellowship.keys()))