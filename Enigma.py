import json

class Enigma:
    def __init__(self, file):
        with open(file, "r") as fh:
            key = json.load(fh)
            self.r1 = key["r1"]
            self.r2 = key["r2"]
            self.r3 = key["r3"]
            self.plugs = key["plugs"]
            self.iteration = key["iteration"]
            self.n = key["n"]
            self.characters = key["characters"]
        
    @staticmethod
    def __rotate(l):
        l.append(l[0])
        l.pop(0)
        return l
    
    
    def __plugin(self, char):
        if len(self.plugs) != 0:
            for i in self.plugs:
                if char in i:
                    return i[1 - i.index(char)]
            else :
                return char
        else:
            return char
    
    def __prerotor(self, char):
        return self.characters.index(char)
    
    def __postrotor(self, char):
        return self.characters[char]

    def __encode(self, char):
        c = self.__plugin(char)
        se = self.__prerotor(c)
        ic = self.r3[self.r2[self.r1[se]]]
        refector = 100 - ic
        fc = self.r1[self.r2[self.r3[refector]]]
        fe = self.__postrotor(fc)
        e = self.__plugin(fe)
        return e
    
    def main(self, character):
        code = self.__encode(character)
        self.iteration += 1
        self.__rotate(self.r1)
        if self.iteration % self.n == 0:
            self.__rotate(self.r2)
        
        if self.iteration % (self.n)**2 == 0:
            self.__rotate(self.r3)
        return code

