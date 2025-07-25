import json

class Rotor:
    def __init__(self, r, p, cls):
        self.iter = cls.iteration
        self.n = cls.n
        if self.iter != 0:
            self.rotor = r[self.iter:] + r[0:self.iter] 
        else :
            self.rotor = r
        self.position = p
    def rotate(self):
        self.rotor.append(self.rotor.pop(0))

    def fcode(self, n):
        if self.iter % (self.n)**self.position == 0:
            self.rotate()
        N = self.rotor[n]
        return N
    
    def bcode(self, n): return self.rotor.index(n)

class plug:
    def __init__(self, p):
        self.fplugs = list(p)
        self.bplugs = list(p)[::-1]
    
    @staticmethod
    def search(pl, char):
        x = pl.index(char) + 1
        return pl[x if x < len(pl) else 0]
    
    def plugs(self, char, mode):
        return self.search(self.fplugs, char) if mode == 0 else self.search(self.bplugs, char)
 
class Enigma:
    def __init__(self, file):
        with open(file, "r", encoding = "utf-8") as fh:
            key = json.load(fh)
            self.number_of_rotors = key["setting"]["number_of_rotor"]
            self.iteration = key["setting"]["iteration"]
            self.n = key["setting"]["n"]
            self.rotor = {}
            for i in range(self.number_of_rotors):
                self.rotor[i] = Rotor(key[key["setting"]["sequence_of_rotor"].split(">")[i]], i, self)
            self.plug = key["setting"]["plugs"]
            self.plugs = {}
            for i in self.plug:
                self.plugs[i] = plug(i)
            self.characters = key["characters"]
    
    def __plugin(self, char, mode = 0):
        for i in self.plug:
            if char in i:
                return self.plugs[i].plugs(char, mode)
        else:
            return char
    
    def __prerotor(self, char):
        return self.characters.index(char)
    
    def __postrotor(self, char):
        return self.characters[char]

    def __encode(self, char):
        c = self.__plugin(char)
        se = self.__prerotor(c)
        for i in self.rotor:
            se = self.rotor[i].fcode(se)
        fc = 99 - se
        for i in range(self.number_of_rotors - 1, -1,-1):
            fc = self.rotor[i].bcode(fc)
        fe = self.__postrotor(fc)
        e = self.__plugin(fe,1)
        return e
    
    def main(self, character):
        code = self.__encode(character)
        self.iteration += 1
            
        return code
