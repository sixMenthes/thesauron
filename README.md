This program requires the libraries:
    - numpy
    - scipy
    - tqdm

It also uses a lot of RAM in full features (60 000 words, fixed-size window= 3, lookbehind= True), so we recommend you to stop any trivial processes.

First copy the corpus in conllu format you want to use for the project in a separate folder. 

Then copy the contents of the current folder (meaning the program)  in the working directory you'll be using. 

Run '''python -i main.py'''. We run it interactively so as to search for synonyms after the program's been executed.

The program will automatically ask you to enter the options, one by one, to build the context dictionary and, later, the matrices.  

Once the dictionary has been built and the matrices calculated, in the interactive mode you can use

'''voisins(word, pos_class)'''

Both the word and the pos class are strings, so don't forget about the string commas! 

Allowed POS classes: 
N for Nouns
V for Verbs
A for Adjectives
ADV for Adverbs


happy holidays :(
