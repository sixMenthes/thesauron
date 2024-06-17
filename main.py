#!/Users/leo/virtualenvs/bin/python3

import os
from tokenbuilder import Token
from dictbuilder import DictionaryBuilding
from tqdm import tqdm
from matrixbuilder import MatrixBuilding


def mainDict(files: list, lookbehind: bool, window= 2):

    dictionary = DictionaryBuilding()

    for file in tqdm(files, desc= 'Creating Dict'):

        with open(file, "r") as file:

            line = file.readline()

            sentence = []

            while line != '':
                sentence.append(Token(line))
                line = file.readline() 
                if line == '\n':
                    dictionary.buildDict(sentence, fsw= window, lookbehind=lookbehind)
                    sentence = []
                    line = file.readline()
        
    dictionary.keepHundred(100)
    print(len(dictionary.ctxt.keys()))

    return dictionary

def mainMatrices(dictionary: DictionaryBuilding):
    
    matrices = MatrixBuilding()
    matrices.fillMatrices(dictionary.ctxt, dictionary.pos)
    matrices.multiplyMatrices()

    return matrices



directory_path = input(str('input path please papá'))
files = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file_name))]

dictionary = mainDict(files, 2, True)
matrices = mainMatrices(dictionary)



print(f"Les synonymes de 'force' sont: ")
matrices.findNeighbors('force', 'N')

print(f"Les synonymes de 'ami' sont: ")
matrices.findNeighbors('ami', 'N')

print(f"Les synonymes de 'tuer' sont: ")
matrices.findNeighbors('tuer', 'V')

print(f"Les synonymes de 'vieux' sont: ")
matrices.findNeighbors('vieux', 'A')

print(f"Les synonymes de 'lentement' sont: ")
matrices.findNeighbors('lentement', 'ADV')

print(f"Les synonymes de 'jouer' sont: ")
matrices.findNeighbors('jouer', 'V')

print(f"Les synonymes de 'fils' sont: ")
matrices.findNeighbors('fils', 'N')

print(f"Les synonymes de 'suspect' sont: ")
matrices.findNeighbors('suspect', 'N')

print(f"Les synonymes de 'gagner' sont: ")
matrices.findNeighbors('gagner', 'V')

print(f"Les synonymes de 'beau' sont: ")
matrices.findNeighbors('beau', 'A')

print(f"Les synonymes de 'subrepticement' sont: ")
matrices.findNeighbors('subrepticement', 'ADV')

print(f"Les synonymes de 'fuir' sont: ")
matrices.findNeighbors('fuir', 'V')






# for key, ctxt in dictionary.ctxt.items():
#     print (key.lemma)
#     for ctxtkey, ctxtcontent in ctxt:
#         print(f"\t {ctxtkey}: {ctxtcontent.lemma}")

print(f"taille dico: {len(dictionary.ctxt.keys())}")


