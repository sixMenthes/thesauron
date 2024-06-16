import os
from hobbiton import Token
from councilOfElrond import DictionaryBuilder


def main(files: list):

    for file in files:

            with open(file, "r") as file:

                line = file.readline()
                sentence = []
                dictionary = DictionaryBuilder()

                while line != '':
                    sentence.append(Token(line))
                    line = file.readline() 
                    if line == '\n':
                        dictionary.insertAndIncrease(sentence)
                        sentence = []
                        line = file.readline() 


    return dictionary
    

directory_path = '/Users/leo/LIL3S2/projet_tal/corpora/test_corpus'
files = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file_name))]

dictionary = main(files)

print(len(dictionary.ctxt))

