import numpy as np
from scipy import sparse
from scipy.sparse.linalg import norm
from tqdm import tqdm
from dictbuilder import DictionaryBuilding
from tokenbuilder import Token


class MatrixBuilding:


    def __init__(self, dictionary: DictionaryBuilding):

        #These are the sets of words, according to the POS tag, transformed into lists to keep the indices straight.  

        self.verb_nlist = list(dictionary.nsetOfVerbs)
        self.name_nlist = list(dictionary.nsetOfNames)
        self.adj_nlist = list(dictionary.nsetOfAdjectives)
        self.adv_nlist = list(dictionary.nsetOfAdverbs)
        

        self.word_nlists = {
            'N': self.name_nlist,
            'V': self.verb_nlist,
            'A': self.adj_nlist, 
            'ADV': self.adv_nlist
        }

        for category in self.word_nlists.keys():
            print(f"size of {category} is {len(self.word_nlists[category])}")

        #These are the sets of contexts, according to the POS tag, transformed into lists to keep the indices straight.  

        self.verb_clist = list(dictionary.cdictOfVerbs.keys())
        self.name_clist = list(dictionary.cdictOfNames.keys())
        self.adj_clist = list(dictionary.cdictOfAdjectives.keys())
        self.adv_clist = list(dictionary.cdictOfAdverbs.keys())

        self.word_clists = {
            'N': self.name_clist,
            'V': self.verb_clist,
            'A': self.adj_clist, 
            'ADV': self.adv_clist
        }

        #now we initialize the sparses matrices according to the dimensions of the lists stated before. 
        #By initializing the matrices in advance we free the computer from having to do memory management and we allow ourselves to fill them with vector operations

        self.verb_matrix = sparse.lil_matrix((len(self.verb_nlist), len(self.verb_clist)), dtype= np.float32)
        self.name_matrix = sparse.lil_matrix((len(self.name_nlist), len(self.name_clist)), dtype= np.float32)
        self.adj_matrix = sparse.lil_matrix((len(self.adj_nlist), len(self.adj_clist)), dtype= np.float32)
        self.adv_matrix = sparse.lil_matrix((len(self.adv_nlist), len(self.adv_clist)), dtype= np.float32)

        self.matrices = {
            'N': self.name_matrix,
            'V': self.verb_matrix,
            'A': self.adj_matrix,
            'ADV': self.adv_matrix
        }

        self.ctxt_dict = dictionary.ctxt 



        

    def fillMatrices (self, dictionary: DictionaryBuilding, weightFun= 'pmi'):

        """The sparse matrices are LIsts of lists (lil) and that allows us to fill them up defining the indices and the values.   """

        for pos_name, matrix in self.matrices.items():

            # create arrays for the row indices, column indices, and values
            row_indices = []
            col_indices = []
            values = []

            for word_idx, word in enumerate(tqdm(self.word_nlists[pos_name], desc= f'Filling {pos_name} matrix ... ')): #loop through the words defined in the word sets that we imported as lists in the __init__ method
                for ctxt_idx, ctxt in enumerate(self.word_clists[pos_name]): #loop through the contexts as well
                    if ctxt in dictionary.ctxt[word]:
                        row_indices.append(word_idx) #fill up the coordinates
                        col_indices.append(ctxt_idx)
                        if weightFun == 'relfreq': #fill up the values according to the weight function.
                            values.append(self.ctxt_dict[word][ctxt] / sum(self.ctxt_dict[word].values())) 
                        elif weightFun == 'pmi':
                            values.append(self.ctxt_dict[word][ctxt] / np.log(dictionary.pos[pos_name][ctxt] * sum(self.ctxt_dict[word].values()))) #dictionary.pos garde le décompte des contextes.
                        else:
                            raise ValueError("Invalid weight function")

            #convert the lists to numpy arrays
            row_indices = np.array(row_indices)
            col_indices = np.array(col_indices)
            values = np.array(values)

            #update the values of the matrix elements using vectorized operations
            matrix[row_indices, col_indices] = values


        
    def multiplyMatrices(self):

        for matrix in tqdm(self.matrices.keys(), desc= 'Multiplying matrices... '):

            #word * ctxt matrix
            sparse_matrix =  self.matrices[matrix].tocsr() #transform the lil matrix into a Compressed Sparse Row array to allow transformations and arithmetic operations
            #normalize the rows so as to get the cosine similarity once we multiply the matrix by its transformed
            row_norms = norm(sparse_matrix, axis=1)
            row_normalized_matrix = sparse_matrix.multiply(1 / row_norms[:, np.newaxis])

            #that we do here
            inverse_matrix = row_normalized_matrix.T
            product = row_normalized_matrix @ inverse_matrix

            #and to an np.array to flatten them and transform them into lists for information retrieval through indexing
            self.matrices[matrix] = product.toarray()

    
    
    def findNeighbors(self, word:str, category: str):


        word_tokenized = Token('')
        word_tokenized.init_for_search(word, category) #Transform the word, category input into a Token as defined in tokenbuilder.py to ease up comparison. 

        if word_tokenized in self.word_nlists[category]: #If we actually know the word.

            word_idx = self.word_nlists[category].index(word_tokenized) #Find the index in the word list with which we made the matrix
            list_of_neighbors = self.matrices[category][word_idx, :].ravel().tolist() #extract the row, flatten it and transform it into a list
            word_to_coeff = list(zip(self.word_nlists[category], list_of_neighbors)) #zip it with the word list, make a single list to sort it and keep them referenced
            sorted_list = sorted(word_to_coeff, key=lambda x: x[1], reverse=True) #sort it

            print(f"Voisins distributionnels de '{word}', {category}:")

            for synonym, coeff in sorted_list[:5]:
                print(f"\t{synonym.lemma}, {np.around(coeff, decimals= 3)}") #print the 5 closest synonyms!
        
        else:
            print("NOT FOUND")

        





    
    
