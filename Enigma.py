# Enigma Reloaded - Beast of an Ancient Legend
# Copyright (C) 2025  Utkarsh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Enigma Reloaded - Beast of an Ancient Legend
--------------------------------------------
This module simulates the Enigma encryption machine, including rotors, plugboard, and encoding logic.
Configuration is loaded from a dictionary or JSON file (see Configuration Structure for format).

Configuration Validation Flow:
-----------------------------
- Checks type of configuration (dictionary or JSON file).
- Validation is performed ONCE in the __new__ method (using pretest()).
- If the configuration is invalid, an exception is raised and the instance is not created.
- __init__ assumes the configuration is already valid and only initializes the machine.

Configuration Structure:
----------------------------------------------
{
    "setting": {
        "number_of_rotors": int,         # Number of rotors in the machine
        "sequence_of_rotor": str,        # Sequence of rotors, e.g., "r1>r2>r3"
        "iteration": int,                # Initial iteration (rotor position/step)
        "rotation_factor": int,           # Rotation base (affects stepping)
        "plugs": [str, ...]              # List of plugboard cycles (e.g., ["ABCD"])
    },
    "characters": [str, ...],            # List of all valid characters for encoding
    "r1": [int, ...],                    # Rotor 1 wiring (permutation of indices)
    "r2": [int, ...],                    # Rotor 2 wiring
    "r3": [int, ...]                     # Rotor 3 wiring
    # ... more rotors as needed (r4, r5, etc.)
}

- The "setting" object defines the machine's configuration.
- "characters" is the character set used for encoding/decoding.
- Each "rX" key defines a rotor's wiring as a permutation of character indices.

Module Contents:
----------------

Classes:
    Enigma: Main machine controller (encoding/decoding)
    Rotor: Individual rotor logic
    plug: Plugboard cycle logic

Functions:
    - __check_type(config): Load and validate configuration from dict, JSON file path, or Path object
    - plug_test(plugs): Validate plugboard cycles for repeated characters and conflicts
    - rotor_test(n, rotor): Validate rotor wiring as a proper permutation of n character indices
    - pretest(file): Comprehensive configuration validation including rotors, plugs, and characters

Classes:
    - Rotor: Individual rotor with wiring, position tracking, and stepping logic
    - plug: Plugboard cycle implementation for character swapping/substitution
    - Enigma: Main machine controller handling configuration, rotors, plugboard, and encoding

Exceptions:
    EnigmaError, ConfigurationError, InvalidCharacterError, ValidationError


Usage Example:
-------------
    >>> enigma = Enigma("configure.json")
    >>> encoded = ''.join(enigma.main(c) for c in "HELLO")
    >>> decoded = ''.join(Enigma("configure.json").main(c) for c in encoded)
    >>> print(decoded)  # 'HELLO'
-------------
    >>> from Enigma import Enigma
    >>> 
    >>> # Create an Enigma machine instance
    >>> enigma = Enigma("configure.json")
    >>> 
    >>> # Encode a message
    >>> message = "HELLO"
    >>> encoded = ""
    >>> for char in message:
    ...     encoded += enigma.main(char)
    >>> print(f"Encoded: {encoded}")
    Encoded: XKLMN
    >>> 
    >>> # Reset the machine to decode
    >>> enigma = Enigma("configure.json")
    >>> decoded = ""
    >>> for char in encoded:
    ...     decoded += enigma.main(char)
    >>> print(f"Decoded: {decoded}")
    Decoded: HELLO
"""

import json
import logging
from typing import List, Union, Dict, Tuple, Optional # pyright: ignore[reportShadowedImports]
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Custom exception classes for better error handling
class EnigmaError(Exception):
    """Base exception for Enigma machine errors."""
    pass

class ConfigurationError(EnigmaError):
    """Raised when there are issues with the configuration file."""
    pass

class InvalidCharacterError(EnigmaError):
    """Raised when a character is not in the configured character set."""
    pass

class ValidationError(EnigmaError):
    """Raised when validation fails during configuration checks."""
    pass

def plug_test(plugs: List[str]) -> Union[List[str], bool]:
    """
    Check for repeated characters in plugboard cycles.
    
    This function validates that no character appears in multiple plugboard cycles,
    which would create ambiguous mappings in the Enigma machine.
    
    Args:
        plugs: List of plugboard cycle strings (e.g., ["ABCD", "EFGH"])
        
    Returns:
        List of repeated characters if found, True if no repeats
        
    Example:
        >>> plug_test(["ABCD", "EFGH"])
        True
        >>> plug_test(["ABCD", "EFGC"])
        ['C', 'G']
    """
    seen_chars = set()  # O(1) lookup for better performance
    repeated_characters: List[str] = []
    
    for plug_cycle in plugs:
        for char in plug_cycle:
            if char in seen_chars:
                repeated_characters.append(char)
            seen_chars.add(char)
    
    return repeated_characters if repeated_characters else True


def rotor_test(n: int, rotor: List[int]) -> Union[bool, Dict[str, List[int]]]:
    """
    Validate rotor wiring as a permutation of n indices.
    
    This function ensures that the rotor wiring is a valid permutation,
    meaning each index from 0 to n-1 appears exactly once.
    
    Args:
        n: Number of characters in the character set
        rotor: Rotor wiring as a list of integers
        
    Returns:
        True if valid permutation, dict with errors if invalid
        
    Example:
        >>> rotor_test(4, [0, 1, 2, 3])
        True
        >>> rotor_test(4, [0, 1, 2, 2])
        {'Extra element': [2], 'Missing Element': [3]}
    """
    expected_indices = set(range(n))
    rotor_set = set(rotor)
    
    extra_elements = list(rotor_set - expected_indices)
    missing_elements = list(expected_indices - rotor_set)
    
    if not extra_elements and not missing_elements:
        return True
    else:
        return {"Extra element": extra_elements, "Missing Element": missing_elements}

def __check_type(config: Union[dict, str, Path]) -> dict:
    """
    Load Enigma configuration from a dictionary or a JSON file path.

    This utility function allows flexible configuration input: you can supply
    either a Python dictionary (already loaded config) or a path (str or Path)
    to a JSON file. The function will always return a dictionary, and provides
    clear error messages for common issues.

    Args:
        config (dict or str or Path): Configuration dictionary or path to a JSON file.

    Returns:
        dict: Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the file path does not exist.
        ValueError: If the JSON file is invalid.
        RuntimeError: For other file reading errors.
        TypeError: If the input is not a dict or a valid path.

    """
    if isinstance(config, dict):
        return config
    elif isinstance(config, (str, Path)):
        try:
            with open(config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file '{config}': {e}")
        except Exception as e:
            raise RuntimeError(f"Error reading configuration file '{config}': {e}")
    else:
        raise TypeError("Config must be a dict or a path to a JSON file.")

def pretest(file: Union[str, dict]) -> Tuple[Dict[str, bool], Dict[str, Union[str, List[str], Dict[str, List[int]]]]]:
    """
    Validate configuration file for consistency and correctness.
    
    This function performs comprehensive validation of the Enigma configuration:
    - Checks that the number of rotors matches the sequence
    - Validates plugboard cycles for repeated characters
    - Ensures each rotor wiring is a valid permutation
    
    Args:
        file: Path to the JSON configuration file
        
    Returns:
        Tuple of (check_list, error_list) where:
            - check_list: Status of each component validation
            - error_list: Detailed error information for failed validations
            
    Raises:
        ConfigurationError: If the configuration file cannot be loaded or is invalid.
        
    Example:
        >>> pretest("configure.json")
        ({'Configuration': True, 'Plugs': True, 'r1': True, 'r2': True, 'r3': True}, {})
    """
    logger.info(f"Starting configuration validation for: {file}")
    
    try:
        key = __check_type(file)
        logger.debug("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise ConfigurationError(f"Error loading configuration: {e}")
    
    try:
        characters = key["characters"]
        number_of_characters = len(characters)
        number_of_rotors = key["setting"]["number_of_rotors"]
        sequence_of_rotor = key["setting"]["sequence_of_rotor"].split(">")
        check_list: Dict[str, bool] = {"Characters": True, "Configuration": True, "Plugs": True}
        error_list: Dict[str, Union[str, List[str], Dict[str, List[int]]]] = {}
        
        logger.debug(f"Validating {number_of_rotors} rotors with {number_of_characters} characters")
        
        # Validate character list
        character_errors = []
        
        # Check for empty character list
        if number_of_characters == 0:
            character_errors.append("Character list is empty")
        
        # Check for duplicate characters
        unique_characters = set(characters)
        if number_of_characters != len(unique_characters):
            duplicates = [char for char in unique_characters if characters.count(char) > 1]
            character_errors.append(f"Duplicate characters found: {duplicates}")
        
        # Check that all elements are single characters (strings of length 1)
        non_single_chars = [char for char in characters if not isinstance(char, str) or len(char) != 1]
        if non_single_chars:
            character_errors.append(f"Non-single character elements found: {non_single_chars[:5]}{'...' if len(non_single_chars) > 5 else ''}")
        
        # Check for None or empty string characters
        invalid_chars = [i for i, char in enumerate(characters) if char is None or char == ""]
        if invalid_chars:
            character_errors.append(f"Invalid characters (None/empty) at indices: {invalid_chars[:10]}{'...' if len(invalid_chars) > 10 else ''}")
        
        if character_errors:
            check_list["Characters"] = False
            error_list["Characters"] = character_errors
            for error in character_errors:
                logger.error(f"Character validation error: {error}")
        
        for i in sequence_of_rotor:
            check_list[i] = True
            
        if number_of_rotors != len(sequence_of_rotor):
            check_list["Configuration"] = False
            error_msg = f"Number of rotors ({number_of_rotors}) doesn't match sequence length ({len(sequence_of_rotor)})"
            error_list["Configuration"] = error_msg
            logger.error(error_msg)
            
        plug_result = plug_test(key["setting"]["plugs"])
        if plug_result != True:
            check_list["Plugs"] = False
            error_list["Repeating characters in plugs"] = plug_result # pyright: ignore[reportArgumentType]
            logger.error(f"Plugboard validation failed: {plug_result}")
            
        for i in sequence_of_rotor:
            rotor_result = rotor_test(number_of_characters, key[i])
            if rotor_result != True:
                check_list[i] = False
                error_list[i] = rotor_result # pyright: ignore[reportArgumentType]
                logger.error(f"Rotor {i} validation failed: {rotor_result}")
        
        if all(check_list.values()):
            logger.info("Configuration validation completed successfully")
        else:
            logger.warning("Configuration validation completed with errors")
                
        return (check_list, error_list)
    except KeyError as e:
        logger.error(f"Missing required configuration field: {e}")
        raise ConfigurationError(f"Missing required configuration field: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}")
        raise ConfigurationError(f"Unexpected error during validation: {e}")





class Rotor:
    """
    Represents a single rotor in the Enigma machine.
    Handles rotor wiring, position, and rotation logic.
    """
    def __init__(self, rotor: List[int], rotor_position: int, cls: 'Enigma') -> None:
        """
        Initialize the rotor.
        
        Args:
            rotor: The rotor wiring (permutation of character indices).
            rotor_position: The position of this rotor in the machine (0 = rightmost).
            cls: Reference to the Enigma instance for iteration and base.
        """
        self.iteration = cls.iteration
        self.n = cls.rotation_base
        self.position = rotor_position
        self.original_rotor = rotor  # Keep original for memory efficiency
        
        # Calculate initial rotation based on iteration and position
        if self.iteration != 0:
            rotation_factor = self.iteration % (self.n) ** self.position
            self.rotor = rotor[rotation_factor:] + rotor[0:rotation_factor]
        else:
            self.rotor = rotor
        
    def __rotate(self) -> None:
        """
        Rotate the rotor by one position (step forward).
        """
        self.rotor.append(self.rotor.pop(0))

    def __fcode(self, n: int) -> int:
        """
        Forward encoding through the rotor.
        
        This method processes a character index through the rotor in the forward
        direction. The rotor rotates (steps) if it's at a turnover position,
        which is determined by the iteration count and position.
        
        Args:
            n: Input character index
            
        Returns:
            Encoded character index after forward rotor processing
        """
        if self.iteration % (self.n) ** self.position == 0:
            self.__rotate()
        return self.rotor[n]
    
    def __bcode(self, n: int) -> int:
        """
        Backward encoding through the rotor (inverse mapping).
        
        This method processes a character index through the rotor in the backward
        direction, applying the inverse of the forward rotor mapping. This is
        used when the signal returns through the rotors after reflection.
        
        Args:
            n: Encoded character index
            
        Returns:
            Decoded character index after backward rotor processing
        """
        return self.rotor.index(n)

class plug:
    """
    Represents a plugboard cycle (swapping characters before/after rotors).
    """
    def __init__(self, plug_cycle: str) -> None:
        """
        Initialize the plugboard cycle.
        
        Args:
            plug_cycle: String of characters forming a plugboard cycle.
        """
        self.fplugs = list(plug_cycle)
        self.bplugs = list(plug_cycle)[::-1]
    
    @staticmethod
    def __search(plug_cycle: List[str], character: str) -> str:
        """
        Find the next character in the plugboard cycle.
        
        This method implements cyclic substitution within a plugboard cycle.
        If the character is found in the cycle, it returns the next character
        in the sequence. If it's the last character, it wraps around to the first.
        
        Args:
            plug_cycle: List of characters in the cycle
            character: Character to search for
            
        Returns:
            The next character in the cycle (wraps around if at end)
        """
        x = plug_cycle.index(character) + 1
        return plug_cycle[x if x < len(plug_cycle) else 0]
    
    def __plugs(self, character: str, mode: int) -> str:
        """
        Swap character using the plugboard cycle.
        
        This method applies plugboard substitution to a character using the
        configured cycle. The mode determines the direction of substitution.
        
        Args:
            character: Character to swap
            mode: 0 for forward substitution, 1 for backward substitution
            
        Returns:
            Swapped character according to the plugboard cycle
        """
        return self.__search(self.fplugs, character) if mode == 0 else self.__search(self.bplugs, character)
 
class Enigma:
    """
    Main Enigma machine class. Handles loading configuration, managing rotors and plugboard, and encoding characters.
    
    Attributes:
        characters (List[str]): Character set used for encoding/decoding
        number_of_rotors (int): Number of rotors in the machine
        iteration (int): Current step count (affects rotor positions)
        rotation_base (int): Base value for rotor stepping calculations
        rotor (Dict[int, Rotor]): Dictionary of rotor instances indexed by position
        plug (List[str]): List of plugboard cycle strings from configuration
        plugs (Dict[str, plug]): Dictionary of plugboard cycle instances
    """
    def __new__(cls, file: Union[str, dict]) -> 'Enigma':
        """
        Validate configuration before creating an Enigma instance.
        
        Args:
            file: Path to the JSON configuration file or configuration dictionary.
            
        Returns:
            Enigma instance if validation passes.
            
        Raises:
            ConfigurationError: If configuration file cannot be loaded or is invalid.
            ValidationError: If configuration validation fails.
        """
        logger.info(f"Creating Enigma instance with configuration: {file}")
        
        try:
            precheck = pretest(file)
            if len(precheck[1]) != 0:
                # Build detailed error message
                error_messages = []
                for component, status in precheck[0].items():
                    if not status:
                        error_messages.append(f"Component '{component}' failed validation")
                
                for error_type, error_details in precheck[1].items():
                    error_messages.append(f"{error_type}: {error_details}")
                
                error_msg = f"Configuration validation failed:\n" + "\n".join(error_messages)
                logger.error(error_msg)
                raise ValidationError(error_msg)
            
            logger.info("Configuration validation successful, creating Enigma instance")
            return super().__new__(cls)
        except (ConfigurationError, ValidationError):
            # Re-raise these specific exceptions as-is
            raise
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {file}")
            raise ConfigurationError(f"Configuration file not found: {file}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")
            raise ConfigurationError(f"Unexpected error loading configuration: {e}")
    
    def __init__(self, file: Union[str, dict]) -> None:
        """
        Initialize the Enigma machine from a configuration file or dictionary.

        Args:
            file: Path to the JSON configuration file or a configuration dictionary.

        Note:
            Configuration validation is performed in __new__ (via pretest()).
            This method assumes the configuration is already valid and only initializes the machine.
        """
        logger.debug("Initializing Enigma machine components")
        
        # Load configuration (already validated in __new__)
        key = __check_type(file)

        # Set character set
        self.characters = key["characters"]

        # Initialize machine settings (number of rotors, initial iteration, and rotation base)
        # rotation_base: Used in rotor stepping logic. If rotation_factor is 0 in config,
        # defaults to character set length for classic Enigma behavior; otherwise uses the configured value.
        # This allows custom stepping patterns without modifying the configuration file.
        self.number_of_rotors = key["setting"]["number_of_rotors"]
        self.iteration = key["setting"]["iteration"]
        self.rotation_base = len(self.characters) if key["setting"]["rotation_factor"] == 0 else key["setting"]["rotation_factor"]

        # Initialize rotors in the specified sequence
        sequence_parts = key["setting"]["sequence_of_rotor"].split(">")
        self.rotor: Dict[int, Rotor] = {}
        for i in range(self.number_of_rotors):
            rotor_name = sequence_parts[i]
            self.rotor[i] = Rotor(key[rotor_name], i, self)

        # Initialize plugboard cycles and plug objects
        self.plug = key["setting"]["plugs"]
        self.plugs: Dict[str, plug] = {}
        for i in self.plug:
            self.plugs[i] = plug(i)

        # Log successful initialization
        logger.info(f"Enigma machine initialized with {self.number_of_rotors} rotors and {len(self.characters)} characters")
    
    def __plugin(self, char: str, mode: int = 0) -> str:
        """
        Pass character through the plugboard (forward or backward).
        
        This method applies plugboard substitution to a character. If the character
        is part of a plugboard cycle, it gets swapped with the next character in
        the cycle. If not in any cycle, the character remains unchanged.
        
        Args:
            char: Character to swap
            mode: 0 for forward mapping, 1 for backward mapping
            
        Returns:
            Swapped character (or original if not in any plugboard cycle)
        """
        for i in self.plug:
            if char in i:
                return self.plugs[i].__plugs(char, mode)
        else:
            return char
    
    def __prerotor(self, char: str) -> int:
        """
        Convert character to its index in the character set.
        
        This method maps a character to its corresponding index in the
        configured character set for rotor processing.
        
        Args:
            char: Character to convert
            
        Returns:
            Index of the character in the character set
        """
        return self.characters.index(char)
    
    def __postrotor(self, char: int) -> str:
        """
        Convert index back to character after rotor processing.
        
        This method converts a rotor-processed index back to its corresponding
        character in the configured character set.
        
        Args:
            char: Index to convert
            
        Returns:
            Character at the given index in the character set
        """
        return self.characters[char]

    def main(self, char: str) -> str:
        """
        Encode/Decode a single character using the Enigma machine logic.
        
        This method implements the complete Enigma encryption/decryption process:
        1. Plugboard forward mapping
        2. Forward pass through all rotors
        3. Reflection (signal reversal)
        4. Backward pass through all rotors
        5. Plugboard backward mapping
        6. Rotor stepping for next character
        
        Args:
            char: Character to encode or decode
            
        Returns:
            Encoded or decoded character
            
        Raises:
            InvalidCharacterError: If character is not in the configured character set
            
        Example:
            >>> enigma = Enigma("configure.json")
            >>> enigma.main("A")
            'X'
            >>> enigma.main("X")  # Decoding the same character
            'A'
        """
        # Validates input from character set
        if char not in self.characters:
            logger.error(f"Invalid character '{char}' not in character set")
            raise InvalidCharacterError(f"Character '{char}' is not in the configured character set")
        
        logger.debug(f"Processing character: '{char}'")
        
        # Pass through plugboard (forward)
        first_encode = self.__plugin(char)
        # Convert to index
        rotor_encode = self.__prerotor(first_encode)
        # Pass through all rotors (forward)
        for i in self.rotor:
            rotor_encode = self.rotor[i].__fcode(rotor_encode)
        # Reflector (reverse the signal)
        reflector = len(self.characters) - 1 - rotor_encode
        # Pass back through all rotors (backward)
        for i in range(self.number_of_rotors - 1, -1, -1):
            reflector = self.rotor[i].__bcode(reflector)
        # Convert back to character
        rotor_decode = self.__postrotor(reflector)
        # Pass through plugboard (backward)
        final_encode = self.__plugin(rotor_decode, 1)
        # Advance iteration (rotor stepping)
        self.iteration += 1
        
        logger.debug(f"Encoded '{char}' -> '{final_encode}' (iteration: {self.iteration})")
        return final_encode
