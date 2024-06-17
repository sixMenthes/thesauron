#!/Users/leo/virtualenvs/bin/python3

import os
from hobbiton import Token
from councilOfElrond import DictionaryBuilder
from tqdm import tqdm
from khazadDum import MatrixBuilding


def main(files: list, lookbehind: bool, window= 2):

    dictionary = DictionaryBuilder()

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



directory_path = '/Users/leo/LIL3S2/projet_tal/corpora/test_corpus'
files = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file_name))]

dictionary = main(files, 2, True)
matrices = MatrixBuilding()
matrices.fillMatrices(dictionary.ctxt, dictionary.pos)
matrices.multiplyMatrices()

# for key, ctxt in dictionary.ctxt.items():
#     print (key.lemma)
#     for ctxtkey, ctxtcontent in ctxt:
#         print(f"\t {ctxtkey}: {ctxtcontent.lemma}")

print(len(dictionary.ctxt.keys()))


