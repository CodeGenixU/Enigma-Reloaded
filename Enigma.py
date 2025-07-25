import json

class Rotor:
    def __init__(self, rotor, rotor_position, cls):
        self.iteration = cls.iteration
        self.n = cls.rotation_base
        self.position = rotor_position
        if self.iteration != 0:
            rotation_factor = self.iteration % (self.n)**self.position
            self.rotor = rotor[rotation_factor:] + rotor[0:rotation_factor] 
        else :
            self.rotor = rotor
        
    def rotate(self):
        self.rotor.append(self.rotor.pop(0))

    def fcode(self, n):
        if self.iteration % (self.n)**self.position == 0:
            self.rotate()
        return self.rotor[n]
    
    def bcode(self, n): 
        return self.rotor.index(n)

class plug:
    def __init__(self, Plug):
        self.fplugs = list(Plug)
        self.bplugs = list(Plug)[::-1]
    
    @staticmethod
    def search(plug_cycle, character):
        x = plug_cycle.index(character) + 1
        return plug_cycle[x if x < len(plug_cycle) else 0]
    
    def plugs(self, character, mode):
        return self.search(self.fplugs, character) if mode == 0 else self.search(self.bplugs, character)
 
class Enigma:
    def __init__(self, file):
        with open(file, "r", encoding = "utf-8") as fh:
            key = json.load(fh)
            self.number_of_rotors = key["setting"]["number_of_rotor"]
            self.iteration = key["setting"]["iteration"]
            self.rotation_base = key["setting"]["n"]
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

    def encode(self, char):
        first_encode = self.__plugin(char)
        rotor_encode = self.__prerotor(first_encode)
        for i in self.rotor:
            rotor_encode = self.rotor[i].fcode(rotor_encode)
        reflector = len(self.characters) - 1 - rotor_encode
        for i in range(self.number_of_rotors - 1, -1,-1):
            reflector = self.rotor[i].bcode(reflector)
        rotor_decode = self.__postrotor(reflector)
        final_encode = self.__plugin(rotor_decode,1)
        self.iteration += 1
        return final_encode
    
