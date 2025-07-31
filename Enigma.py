"""
Enigma Reloaded - Beast of an Ancient Legend
-----------------------
This module simulates the Enigma encryption machine, including rotors, plugboard, and encoding logic.
Configuration is loaded from a JSON file (see configure.json for format).

Configuration File (configure.json) Structure:
----------------------------------------------
{
    "setting": {
        "number_of_rotors": int,         # Number of rotors in the machine
        "sequence_of_rotor": str,       # Sequence of rotors, e.g., "r1>r2>r3"
        "iteration": int,               # Initial iteration (rotor position/step)
        "n": int,                       # Rotation base (affects stepping)
        "plugs": [str, ...]             # List of plugboard cycles (e.g., ["ABCD"])
    },
    "characters": [str, ...],           # List of all valid characters for encoding
    "r1": [int, ...],                   # Rotor 1 wiring (permutation of indices)
    "r2": [int, ...],                   # Rotor 2 wiring
    "r3": [int, ...]                    # Rotor 3 wiring
    // ... more rotors as needed
}

- The "setting" object defines the machine's configuration.
- "characters" is the alphabet used for encoding/decoding.
- Each "rX" key defines a rotor's wiring as a permutation of character indices.
"""
import json

class Rotor:
    """
    Represents a single rotor in the Enigma machine.
    Handles rotor wiring, position, and rotation logic.
    """
    def __init__(self, rotor, rotor_position, cls):
        """
        Initialize the rotor.
        Args:
            rotor (list): The rotor wiring (permutation of character indices).
            rotor_position (int): The position of this rotor in the machine (0 = rightmost).
            cls (Enigma): Reference to the Enigma instance for iteration and base.
        """
        self.iteration = cls.iteration
        self.n = cls.rotation_base
        self.position = rotor_position
        # Calculate initial rotation based on iteration and position
        if self.iteration != 0:
            rotation_factor = self.iteration % (self.n)**self.position
            self.rotor = rotor[rotation_factor:] + rotor[0:rotation_factor] 
        else :
            self.rotor = rotor
        
    def rotate(self):
        """
        Rotate the rotor by one position (step forward).
        """
        self.rotor.append(self.rotor.pop(0))

    def fcode(self, n):
        """
        Forward encoding through the rotor.
        Rotates if at a turnover position.
        Args:
            n (int): Input character index.
        Returns:
            int: Encoded character index.
        """
        if self.iteration % (self.n)**self.position == 0:
            self.rotate()
        return self.rotor[n]
    
    def bcode(self, n): 
        """
        Backward encoding through the rotor (inverse mapping).
        Args:
            n (int): Encoded character index.
        Returns:
            int: Decoded character index.
        """
        return self.rotor.index(n)

class plug:
    """
    Represents a plugboard cycle (swapping characters before/after rotors).
    """
    def __init__(self, Plug):
        """
        Initialize the plugboard cycle.
        Args:
            Plug (str): String of characters forming a plugboard cycle.
        """
        self.fplugs = list(Plug)
        self.bplugs = list(Plug)[::-1]
    
    @staticmethod
    def search(plug_cycle, character):
        """
        Find the next character in the plugboard cycle.
        Args:
            plug_cycle (list): List of characters in the cycle.
            character (str): Character to search for.
        Returns:
            str: The next character in the cycle.
        """
        x = plug_cycle.index(character) + 1
        return plug_cycle[x if x < len(plug_cycle) else 0]
    
    def plugs(self, character, mode):
        """
        Swap character using the plugboard cycle.
        Args:
            character (str): Character to swap.
            mode (int): 0 for forward, 1 for backward.
        Returns:
            str: Swapped character.
        """
        return self.search(self.fplugs, character) if mode == 0 else self.search(self.bplugs, character)
 
class Enigma:
    """
    Main Enigma machine class. Handles loading configuration, managing rotors and plugboard, and encoding characters.
    """
    def __init__(self, file):
        """
        Initialize the Enigma machine from a configuration file.
        Args:
            file (str): Path to the JSON configuration file.
        """
        with open(file, "r", encoding = "utf-8") as fh:
            key = json.load(fh)
            self.number_of_rotors = key["setting"]["number_of_rotor"]
            self.iteration = key["setting"]["iteration"]
            self.rotation_base = key["setting"]["n"]
            self.rotor = {}
            # Initialize rotors in the specified sequence
            for i in range(self.number_of_rotors):
                self.rotor[i] = Rotor(key[key["setting"]["sequence_of_rotor"].split(">")[i]], i, self)
            self.plug = key["setting"]["plugs"]
            self.plugs = {}
            # Initialize plugboard cycles
            for i in self.plug:
                self.plugs[i] = plug(i)
            self.characters = key["characters"]
    
    def __plugin(self, char, mode = 0):
        """
        Pass character through the plugboard (forward or backward).
        Args:
            char (str): Character to swap.
            mode (int): 0 for forward, 1 for backward.
        Returns:
            str: Swapped character (or original if not in any plug).
        """
        for i in self.plug:
            if char in i:
                return self.plugs[i].plugs(char, mode)
        else:
            return char
    
    def __prerotor(self, char):
        """
        Convert character to its index in the character set.
        Args:
            char (str): Character to convert.
        Returns:
            int: Index of the character.
        """
        return self.characters.index(char)
    
    def __postrotor(self, char):
        """
        Convert index back to character after rotors.
        Args:
            char (int): Index to convert.
        Returns:
            str: Character at the given index.
        """
        return self.characters[char]

    def main(self, char):
        """
        Encode/Decode a single character using the Enigma machine logic.
        Args:
            char (str): Character to encode or decode.
        Returns:
            str: Encoded or decoded character.
        """
        # Pass through plugboard (forward)
        first_encode = self.__plugin(char)
        # Convert to index
        rotor_encode = self.__prerotor(first_encode)
        # Pass through all rotors (forward)
        for i in self.rotor:
            rotor_encode = self.rotor[i].fcode(rotor_encode)
        # Reflector (reverse the signal)
        reflector = len(self.characters) - 1 - rotor_encode
        # Pass back through all rotors (backward)
        for i in range(self.number_of_rotors - 1, -1,-1):
            reflector = self.rotor[i].bcode(reflector)
        # Convert back to character
        rotor_decode = self.__postrotor(reflector)
        # Pass through plugboard (backward)
        final_encode = self.__plugin(rotor_decode,1)
        # Advance iteration (rotor stepping)
        self.iteration += 1
        return final_encode
    
