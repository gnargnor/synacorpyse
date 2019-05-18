class Memory:
    @property
    def tokens(self):
        return self.__tokens

    def __init__(self, tokens):
        self.__tokens = tokens

    def gen_next(self, address=0):
        limit = len(self.tokens) - address

        while address < limit:
            yield self.tokens[address]
            address += 1


