import numpy as np
from scipy.sparse import csr_matrix
from tqdm import tqdm

class MatrixBuilding:

    def __init__(self, context_sets: dict, context_dict: dict):

        self.name_matrix = []
        self.verb_matrix = []
        self.adj_matrix = []
        self.adv_matrix = []

        self.word_matrices = {
            'N': self.name_matrix,
            'V': self.verb_matrix,
            'A': self.adj_matrix, 
            'ADV': self.adv_matrix
        }

    def fillMatrices (self, dictionary: dict, posSet: dict):

        for word in tqdm(dictionary.keys(), desc='filling matrices'):

            word_vec = np.zeros(len(posSet[word.cat]))

            for idx, context in enumerate(posSet[word.cat]):

                if context in dictionary[word].keys():
                    word_vec[idx] = dictionary[word][context]
                
                else:
                    word_vec[idx] = 0
            
            self.word_matrices[word.cat].append(word_vec)

        for matrix in self.word_matrices.keys():
            self.word_matrices[matrix] = np.stack(matrix, axis=0)
        
        return self.word_matrices


    def multiplyMatrices(self):

        for matrix in tqdm(self.word_matrices.keys(), desc= 'multiplying matrices'):
            normal_matrix = self.word_matrices[matrix]
            print(normal_matrix.shape)
            inverse_matrix = self.word_matrices[matrix].T
            print(inverse_matrix.shape)
            product = csr_matrix(normal_matrix) * csr_matrix(inverse_matrix)
            self.word_matrices[matrix] = product.todense()
            print(self.word_matrices[matrix].shape)

        return self.word_matrices