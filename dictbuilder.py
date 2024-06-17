from hobbiton import Token



class DictionaryBuilding:

    def __init__ (self):

        self.verbs = set()
        self.names = set()
        self.adjectives = set()
        self.adverbs = set()

        self.pos = {
            'V': self.verbs,
            'N': self.names,
            'A': self.adjectives,
            'ADV': self.adverbs
        }

        self.ctxt = {}
        self.counts = {}
            
                    
    
    def lookbehindFun (self, cur_word: Token, idx: int, sentence: list, fsw: int):

        prev_idx = 1

        while prev_idx <= fsw:
            context = (f"-{prev_idx}", sentence[idx - prev_idx])
            self.pos[cur_word.cat].add(context)
            self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1
            prev_idx += 1
    
    def lookforwardFun(self, cur_word: Token, idx: int, sentence: list, fsw: int):

        post_idx = 1

        while post_idx <= fsw:
            context = (f"+{post_idx}", sentence[idx + post_idx])
            self.pos[cur_word.cat].add(context)
            self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1
            post_idx += 1



    def buildDict(self, sentence: list, fsw: int, lookbehind= True):

        if len(self.ctxt.keys()) < 60000:

            sentence = [Token('<d>')] * fsw + sentence + [Token('<f>')] * fsw

            for cur_idx, cur_word in enumerate(sentence):

                if cur_word.cat in self.pos.keys():

                    self.ctxt.setdefault(cur_word, dict())
                    self.counts[cur_word] = self.counts.get(cur_word, 0) + 1
                    self.lookforwardFun(cur_word, cur_idx, sentence, fsw)

                    if lookbehind == True:

                        self.lookbehindFun(cur_word, cur_idx, sentence, fsw)
        else:
            self.increaseDict(sentence, fsw, lookbehind)
            
    
    def increaseDict(self, sentence: list, fsw: int, lookbehind= True):

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



