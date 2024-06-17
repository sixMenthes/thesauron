import numpy as np
from scipy import sparse
from scipy.sparse.linalg import norm
from tqdm import tqdm


class MatrixBuilding:


    def __init__(self):

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

        self.verb_list = []
        self.name_list = []
        self.adj_list = []
        self.adv_list = []

        self.word_lists = {
            'N': self.name_list,
            'V': self.verb_list,
            'A': self.adj_list, 
            'ADV': self.adv_list
        }


        

    def fillMatrices (self, dictionary: dict, posSet: dict):

        for word in tqdm(dictionary.keys(), desc='filling matrices'):

            self.word_lists[word.cat].append(word.lemma)
            word_vec = np.zeros(len(posSet[word.cat]))

            for idx, context in enumerate(posSet[word.cat]):

                if context in dictionary[word]:
                    word_vec[idx] = dictionary[word][context]/sum(dictionary[word].values())


               
                else:
                    word_vec[idx] = 0
            
            self.word_matrices[word.cat].append(word_vec)

        for name, value in self.word_matrices.items():
            self.word_matrices[name] = sparse.coo_array(value)
        
        return self.word_matrices
    
    
    def multiplyMatrices(self):

        for matrix in tqdm(self.word_matrices.keys(), desc= 'multiplying matrices'):

            #word * ctxt
            sparse_matrix =  self.word_matrices[matrix].tocsr()
            print(sparse_matrix.shape)
            row_norms = norm(sparse_matrix, axis=1)
            row_normalized_matrix = sparse_matrix.multiply(1 / row_norms[:, np.newaxis])

            #ctxt * word
            inverse_matrix = row_normalized_matrix.T.tocsr()
            print(inverse_matrix.shape)

            #word * word
            product = row_normalized_matrix @ inverse_matrix

            self.word_matrices[matrix] = product.todense()
            print(self.word_matrices[matrix].shape)

        return self.word_matrices
    
    
    def findNeighbors(self, word:str, categorie: str):

        if word in self.word_lists[categorie]:

            word_idx = self.word_lists[categorie].index(word)

            neighbor_list = list(self.word_matrices[categorie][word_idx])

            word_to_coeff = list(zip(self.word_lists[categorie], neighbor_list))

            sorted_list = sorted(word_to_coeff, key=lambda x: x[1], reverse=True)

            print(sorted_list[:5])
        
        else:
            print("NOT FOUND")

        





    
    
