from tokenbuilder import Token

"""Most attributes are embedded in a dictionary whose keys are the POS tags we can find in Tokens as defined in tokenbuilder.py. This eased up a lot the coding. """


class DictionaryBuilding:

    def __init__ (self):

        #These are the dictionaries of contexts according to POS tag. They're useful to get the total number of contexts, but it also stores the counts for each context which
        # will be necessary to calculate the PMI weight function.

        self.cdictOfVerbs = dict()
        self.cdictOfNames = dict()
        self.cdictOfAdjectives = dict()
        self.cdictOfAdverbs = dict()

        self.pos = {
            'V': self.cdictOfVerbs,
            'N': self.cdictOfNames,
            'A': self.cdictOfAdjectives,
            'ADV': self.cdictOfAdverbs
        }

        #These are the set of words according to POS tag. They're useful.

        self.nsetOfVerbs = set()
        self.nsetOfNames = set()
        self.nsetOfAdjectives = set()
        self.nsetOfAdverbs = set()

        self.wordset = {
            'V': self.nsetOfVerbs,
            'N': self.nsetOfNames,
            'A': self.nsetOfAdjectives,
            'ADV': self.nsetOfAdverbs
        }

        #These are the proper dictionary, self.ctxt, and a dictionary of word counts, self.counts, to
        #clean self.ctxt of all words that have less than x counts with the method DictionaryBuilding.keepHundred(x)

        self.ctxt = {}
        self.counts = {}
            
    """For both lookbehindFun and lookforwardFun we simply use a cursor to iterate on the text starting at the current word (forwards or backwards)."""
    
    def lookbehindFun (self, cur_word: Token, idx: int, sentence: list, fsw: int):

        prev_idx = 1

        while prev_idx <= fsw:
            context = (f"-{prev_idx}", sentence[idx - prev_idx])
            self.pos[cur_word.cat][context] = self.pos[cur_word.cat].get(context, 0) + 1 #update the context:counts dictionary
            self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1 #update the word:contexs:counts dictionary
            prev_idx += 1
    
    def lookforwardFun(self, cur_word: Token, idx: int, sentence: list, fsw: int):

        post_idx = 1

        while post_idx <= fsw:
            context = (f"+{post_idx}", sentence[idx + post_idx])
            self.pos[cur_word.cat][context] = self.pos[cur_word.cat].get(context, 0) + 1 #update the context:counts dictionary
            self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1 #update the word:contexs:counts dictionary
            post_idx += 1


    """buildDict and increaseDict make very similar stuff, the only difference beeing that increaseDict doesn't add new word entries to the context dictionary. """



    def buildDict(self, sentence: list, threshold: int, fsw= 2, lookbehind= True):

        if len(self.ctxt.keys()) < threshold:

            sentence = [Token('<d>')] * fsw + sentence + [Token('<f>')] * fsw #So as not to get an index out of bounds, since we iterate on the text to find the contexts we 
        #have to add false tokens at the beginning and at the end according to the fixed-size window.

            for cur_idx, cur_word in enumerate(sentence):

                if cur_word.cat in self.pos.keys(): #if the word categry is amongst Names, Verbs, Adjectives, Adverbes. We're eliminating function words. 

                    self.ctxt.setdefault(cur_word, dict()) #insert the word in the dict
                    self.counts[cur_word] = self.counts.get(cur_word, 0) + 1 #increase its counts in the counts dictionary (useful for keepHundred function)
                    self.lookforwardFun(cur_word, cur_idx, sentence, fsw) 

                    if lookbehind == True:

                        self.lookbehindFun(cur_word, cur_idx, sentence, fsw)
        else:
            self.increaseDict(sentence, fsw, lookbehind)
        

            
    
    def increaseDict(self, sentence: list, fsw= 2, lookbehind= True):

        sentence = [Token('<d>')] * fsw + sentence + [Token('<f>')] * fsw 

        for cur_idx, cur_word in enumerate(sentence):

            if (cur_word.cat in self.pos.keys()) and (cur_word in self.ctxt.keys()):

                self.counts[cur_word] = self.counts.get(cur_word, 0) + 1
                self.lookforwardFun(cur_word, cur_idx, sentence, fsw)

                if lookbehind == True:

                    self.lookbehindFun(cur_word, cur_idx, sentence, fsw)
                


    def keepHundred(self, threshold: int):
        keys_to_remove = [word for word, count in self.counts.items() if count < threshold]
        for key in keys_to_remove:
            del self.ctxt[key]
            del self.counts[key]
        for key in self.ctxt.keys():
            self.wordset[key.cat].add(key) #here we wished to create a set of words to ease up our work in the matrix building part. 
            #It'll be easier to find the word indexes and update the matrix accordingly.



