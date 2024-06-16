from hobbiton import Token

class DictionaryBuilder:

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


    def insertAndIncrease(self, sentence: list, fsw= 2, lookbehind= True):

        sentence = [Token('<d>') for i in range(fsw)] + sentence + [Token('<f>') for i in range(fsw)]

        for idx, cur_word in enumerate(sentence):
            
            if cur_word.cat in self.pos.keys():

                self.ctxt.setdefault(cur_word, dict())
                self.counts[cur_word] = self.counts.get(cur_word, 0) + 1

                post_idx = 1

                while post_idx <= fsw:
                    context = (f"+{post_idx}", sentence[idx + post_idx])
                    self.pos[cur_word.cat].add(context)
                    self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1
                    post_idx += 1
                
                if lookbehind == True:

                    prev_idx = 1

                    while prev_idx <= fsw:
                        context = (f"-{prev_idx}", sentence[idx - prev_idx])
                        self.pos[cur_word.cat].add(context)
                        self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1
                        prev_idx += 1

    def increase(self, sentence: list, fsw= 2, lookbehind= True):

        sentence = [Token('<d>') for i in range(fsw)] + sentence + [Token('<f>') for i in range(fsw)]

        for idx, cur_word in enumerate(sentence):
            
            if cur_word in self.counts.keys():
                self.counts[cur_word] = self.counts.get(cur_word, 0) + 1

                post_idx = 1

                while post_idx <= fsw:
                    context = (f"+{post_idx}", sentence[idx + post_idx])
                    self.pos[cur_word.cat].add(context)
                    self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1
                    post_idx += 1
                
                if lookbehind == True:

                    prev_idx = 1

                    while prev_idx <= fsw:
                        context = (f"-{prev_idx}", sentence[idx - prev_idx])
                        self.pos[cur_word.cat].add(context)
                        self.ctxt[cur_word][context] = self.ctxt[cur_word].get(context, 0) + 1
                        prev_idx += 1

