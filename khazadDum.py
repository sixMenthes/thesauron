import numpy as np

def minesOfMoria (fellowship: dict, the_ring: dict):

    name_matrix = []
    verb_matrix = []
    adj_matrix = []
    adv_matrix = []

    matricesOfMoria = {
        'N': name_matrix,
        'V': verb_matrix,
        'A': adj_matrix, 
        'ADV': adv_matrix
    }

    for word in fellowship.keys():
        word_vec = np.zeros(len(the_ring[word.category]))
        for idx, context in enumerate(the_ring[word.category]):
            if context in fellowship[word].keys():
                word_vec[idx] = fellowship[word][context]
            else:
                word_vec[idx] = 0
        matricesOfMoria[word.category].append(word_vec)

    for matrix in matricesOfMoria.values():
        np.stack(matrix, axis=1)
    
    return matricesOfMoria


def balrogMultiplication(word_matrices: dict):
    for matrix in word_matrices.keys:
        word_matrices[matrix] = matrix @ matrix.T
    return word_matrices