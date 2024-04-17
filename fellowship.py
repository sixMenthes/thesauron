'''
We start by importing Sam, who'll carry all the important stuff ! Sam.index gives the index in the sentence, Sam.lemma gives the lemma...
'''
from hobbiton import Shire

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


with open('/Users/leo/LIL3S2/projet_tal/estrepublicain.extrait-aa.19998.outmalt', "r") as conllu:
    text = Shire(conllu.read())


fellowship = dict()
the_ring = set()

for sentence in text.sentences:
    andmyBOW(sentence, fellowship, the_ring, bow= 2)

