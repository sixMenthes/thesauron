from tokenbuilder import Token
from dictbuilder import DictionaryBuilding
from matrixbuilder import MatrixBuilding
from tqdm import tqdm
import os

"""This is the main file of our thesaurus program."""

directory_path = str(input("Input the /path/to/directory \n"))
files = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file_name))]
print("Start by choosing the options for the context dictionary.\n")
fixed_size_window = int(input("Input the size of the fixed size window.\n"))
lookbehind = str(input("Do you wish the context dictionary to take into account the contexts preceding the words? True/False\n"))
dict_max_size = int(input("Input the maximum size of the context dictionary. How many words should it keep?\n"))
weight_function = int(input("Choose the weight function: enter 0 to use RelFreq and 1 to use PMI\n"))



def mainDict(files: list, lookbehind: bool, dict_max_size=60000, window= 2):
    
    """This function loops over the files referenced by the directory path. It reads the documents line by line 
    so as not to overcharge the ram. We thus avoid juggling. Once a sentence has been completed, the buildDict function processes it so as to build the context dictionary
    (and adjacent necessary data structures). """

    dictionary = DictionaryBuilding() #We first initialize our data structure.

    for file in tqdm(files, desc= 'Creating Dict'):

        with open(file, "r") as file:

            line = file.readline()

            sentence = []

            while line != '':
                sentence.append(Token(line))
                line = file.readline() 
                if line == '\n':
                    dictionary.buildDict(sentence, dict_max_size, fsw= fixed_size_window, lookbehind=lookbehind)
                    sentence = []
                    line = file.readline()
        
    dictionary.keepHundred(100) #This method ensures that all dictionary entries with less than 100 occurrences are erased. It is an essential step according to Henstroza
    return dictionary

def mainMatrices(dictionary: DictionaryBuilding, weightFun= 1):

    """Initialize our MatrixBuilding class importing information from the DictionaryBuilding object. Weight function can be chosen."""
    
    matrices = MatrixBuilding(dictionary)

    if weightFun == 0:
        matrices.fillMatrices(dictionary, 'relfreq')
    elif weightFun == 1:
        matrices.fillMatrices(dictionary, 'pmi')
    else:
        raise ValueError('Weight function unknown')
     
    matrices.multiplyMatrices()

    return matrices

def voisins(word: str, category: str): #Cette fonction ne sert qu'à renommer pour rendre la commande plus simple
    
    return matrices.findNeighbors(word, category)


dictionary = mainDict(files, fixed_size_window, dict_max_size, lookbehind)
matrices = mainMatrices(dictionary, weight_function)








