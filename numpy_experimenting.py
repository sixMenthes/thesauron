import numpy as np
lemmas = []
contexts = []

lemma_to_index = {lemma: i for i, lemma in enumerate(lemmas)}
context_to_index = {context: i for i, context in enumerate(contexts)}

NxC = np.zeros((len(lemmas), len(contexts)))

for lemma, context in [('lemma1', 'context1'), ('lemma2', 'context2'), ('lemma3', 'context3')]:
    NxC[lemma_to_index[lemma], context_to_index[context]] = 1

print(NxC)
