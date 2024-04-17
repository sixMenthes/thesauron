'''
I believe for now we just wanna keep the lemmas, right ? This is pretty sketchy, but we will make it prettier. The idea is 
to output a list of lemmas following the order of the words in the document est-republicain. each sentence is separated by an empty string. 
'''

def extractLemma(token:str):
    if token == '':
        return ''
    else:
        return token.split('\t')[2]

def conlluReader (path: str) -> list:
    #outputs a list of strings. Each member is a lemma following the order of the corpus sentences. Each sentence of the corpus is separated by an empty string.
    with open(path, "r") as conllu:
        post_text = []
        for token in conllu.read().split("\n"):
            post_text.append(extractLemma(token))
    return post_text 

def dictBuilder (text: list):
    #returns a dictionary of dictionaries. Keys are words, values are dicts of <keys = contexts, values = counts>
    fellowship = dict()
    for index, word in enumerate(text):
        fellowship.setdefault(word, dict())
        #print(index)

        if (index == 0) or (text[index-1] == ''):

            #print('word = ' + word)
            fellowship[word][(+1, text[index+1])] = fellowship[word].get(('+1', text[index+1]), 0) + 1

        if (index == -1) or (text[index+1] == ''):

            fellowship[word][(-1, text[index-1])] = fellowship[word].get(('-1', text[index-1]), 0) + 1

        else :
            fellowship[word][(+1, text[index+1])] = fellowship[word].get(('+1', text[index+1]), 0) + 1
            fellowship[word][(-1, text[index-1])] = fellowship[word].get(('-1', text[index-1]), 0) + 1
    
    return fellowship




conllu_doc = '/Users/leo/LIL3S2/projet_tal/estrepublicain.extrait-aa.19998.outmalt'
processed_text = conlluReader(conllu_doc)
#print(processed_text[19996], processed_text[19997], processed_text[19998])
print(processed_text)
#test_dict = dictBuilder(processed_text)

#print(test_dict)

        


