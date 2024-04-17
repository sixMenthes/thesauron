'''
I believe for now we just wanna keep the lemmas, right ? This is pretty sketchy, but we will make it prettier. The idea is 
to output a list of lemmas following the order of the words in the document est-republicain. each sentence is separated by an empty string. 
'''

def extractLemma(line:str):
    return line.split('\t')[2]

with open('/Users/leo/LIL3S2/projet_tal/estrepublicain.extrait-aa.19998.outmalt', "r") as conllu:
    


def conlluReader (path: str) -> list:
    #outputs a list of strings. Each member is a lemma following the order of the corpus sentences. Each sentence of the corpus is separated by an empty string.
    with open(path, "r") as conllu:
        post_text = []
        for token in conllu.read().split("\n"):
            post_text.append(extractLemma(token))
    return post_text 


