'''
We start by importing Sam, who'll carry all the important stuff ! Sam.index gives the index in the sentence, Sam.lemma gives the lemma...
'''
from sam import Sam, Shire

with open('/Users/leo/LIL3S2/projet_tal/estrepublicain.extrait-aa.19998.outmalt', "r") as conllu:
    text = Shire(conllu.read())

def andmyBOW(sentence: list, fellowship: dict, bag_of_words = 1):
    for idx, cur_word in enumerate(sentence):
        fellowship.setdefault(cur_word.lemma, dict())
        for prev_word in sentence[idx - bag_of_words: idx]:
            



#def andmyBOW(bag_of_words = 1):
#    for sentence in text.sentences:


# def andMyBow(window = 1):

#     fellowship = dict()

#     with open('/Users/leo/LIL3S2/projet_tal/estrepublicain.extrait-aa.19998.outmalt', "r") as conllu:
#         text = conllu.read().split("\n").remove('')
#         for idx, line in enumerate(text):
#             cur_word = Sam(line)
#             fellowship.setdefault(cur_word.lemma, dict())
#             if (idx - window >= 0) and (idx + window <= len(text)+1):
#                 for prev_word in text[idx - window: idx + 1]:

