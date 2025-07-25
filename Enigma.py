import json

class Enigma:
    def __init__(self, file):
        with open(file, "r", encoding = "utf-8") as fh:
            key = json.load(fh)
            self.number_of_rotors = key["setting"]["number_of_rotor"]
            self.iteration = key["setting"]["iteration"]
            self.n = key["setting"]["n"]
            self.rotor = []
            for i in key["setting"]["sequence_of_rotor"].split(">"):
                self.rotor.append(key[i])
            self.plugs = key["setting"]["plugs"]
            self.characters = key["characters"]

            if self.iteration != 0:
                for i in range(self.number_of_rotors):
                    rot_count = (self.iteration // (self.n)**i) % 100
                    self.rotor[i] = self.rotor[i][rot_count:] + self.rotor[i][:rot_count]
    @staticmethod
    def __rotate(l):
        l.append(l.pop(0))
        return l
    
    
    def __plugin(self, char):
        return self.plugs.get(char, char)
    
    def __prerotor(self, char):
        return self.characters.index(char)
    
    def __postrotor(self, char):
        return self.characters[char]

    def __encode(self, char):
        c = self.__plugin(char)
        se = self.__prerotor(c)
        for i in self.rotor:
            se = i[se]
        fc = 99 - se
        for i in self.rotor.copy()[::-1]:
            fc = i.index(fc)
        fe = self.__postrotor(fc)
        e = self.__plugin(fe)
        return e
    
    def main(self, character):
        code = self.__encode(character)
        self.iteration += 1
        for i in range(self.number_of_rotors):
            if self.iteration % (self.n)**i == 0:
                self.__rotate(self.rotor[i])
        return code


