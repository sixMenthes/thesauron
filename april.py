def extractContext(sentence: conll.sentence, word: token):
    if word.index -1 > 0:
        bigram1 = ('-1', (sentence[word.index - 1].lemma, sentence[word.index - 1].pos))
    else:
        bigram1 = None    
    if word.index + 1 < sentence.length:    
        bigram2 = ('+1', (sentence[word.index + 1].lemma, sentence[word.index + 1].pos))
    else: 
        bigram2 = None    
    return bigram1, bigram2

