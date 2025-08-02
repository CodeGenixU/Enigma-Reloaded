# Enigma Reloaded

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-GPLv3-blue)
![Status](https://img.shields.io/badge/status-stable-green)

**Beast of an Ancient Legend**

---

## Table of Contents
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Configuration Rules](#configuration-rules)
- [Usage](#usage)
- [Module Contents](#module-contents)
- [Error Handling](#error-handling)
- [Requirements](#requirements)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Author](#author)
- [Disclaimer](#disclaimer)
- [Special Message](#special-message)
---

This project is not a classic Enigma simulation, but an advanced, extensible cryptographic machine. While its core draws inspiration from the legendary Enigma, this implementation is fundamentally different and vastly more powerful. It features a highly flexible architecture, supporting arbitrary character sets, customizable rotor logic, advanced plugboard cycles, and modern validation and configuration mechanisms.

Enigma Reloaded is designed for cryptographers, researchers, and enthusiasts seeking a customizable, state-of-the-art encryption engine that goes far beyond historical limitations.

## Key Features

- **Highly Configurable Architecture:** Supports any number of rotors, each with fully custom wiring (permutation of indices).
- **Advanced Plugboard System:** Allows multiple variable length disjoint plugboard cycles for additional scrambling.
- **Universal Character Set:** Encode and decode using any set of characters, including Unicode, symbols, and custom alphabets.
- **Modern JSON & Dictionary Configuration:** All settings are loaded from a human-readable JSON file or a nested dictionary for maximum flexibility.
- **Robust Validation:** Comprehensive configuration checks and error handling ensure cryptographic soundness.
- **Extensible Design:** Built for experimentation, research, and real-world cryptographic applications.
- **Logging and Debugging:** Integrated logging for deep inspection and validation feedback.
- **Open Source:** Licensed under the GNU GPL v3.

---

## Quick Start

1. **Clone or download this repository.**
2. Ensure you have Python 3.7+ installed.
3. (Optional) Create and activate a virtual environment.
4. No external dependencies are required; all modules use Python standard library.
5. Run the example below or your own script using the Enigma engine.

```python
from Enigma import Enigma

enigma = Enigma("configure.json")
message = "HELLO"
encoded = ""
for char in message:
    encoded += enigma.main(char)
print(f"Encoded: {encoded}")

enigma = Enigma("configure.json")
decoded = ""
for char in encoded:
    decoded += enigma.main(char)
print(f"Decoded: {decoded}")
```

---

## Configuration

The Enigma machine is configured via a nested dictionary or a JSON file (see `configure.json` for an example):

```json
{
    "setting": {
        "number_of_rotors": 3,
        "sequence_of_rotor": "r1>r2>r3",
        "iteration": 25,
        "rotation_factor": 3,
        "plugs": ["ABCD", "@[{()}]?", "0123456789"]
    },
    "characters": ["0", "1", "2", ..., "z", "A", ..., "Z", "!", ..., "•", "£", "¥"],
    "r1": [ ... ],
    "r2": [ ... ],
    "r3": [ ... ]
}
```

- **r1:** Rotor 1 wiring (permutation of indices)
- **r2:** Rotor 2 wiring
- **r3:** Rotor 3 wiring
- **number_of_rotors:** Number of rotors in the machine.
- **sequence_of_rotor:** Order of rotors (e.g., `"r1>r2>r3"`).
- **iteration:** Initial step count for rotor stepping.
- **rotation_factor:** Rotation base (affects stepping).
- **plugs:** List of plugboard cycles (e.g., `["ABCD", "@[{()}]?", "0123456789"]`).
- **characters:** List of all valid characters for encoding.
- **rX:** Each rotor's wiring as a permutation of character indices.

---

## Configuration Rules

When creating or editing your `configure.json` file or a nested dictionary, follow these rules for correct operation:

1. **Characters List**
   - Must be a list of unique characters (no duplicates).
   - The length of this list determines the size of each rotor and the valid input set.
   - All characters you wish to encode/decode must be included here.

2. **Rotors (`r1`, `r2`, etc.)**
   - Each rotor must be a permutation of the indices `0` to `N-1`, where `N` is the length of the characters list.
   - No repeated or missing indices are allowed.
   - The number of rotors must match `number_of_rotors`.

3. **Plugboard (`plugs`)**
   - Each plugboard cycle is a string of characters (e.g., `"ABCD"`).
   - No character should appear in more than one cycle or more than once per cycle.
   - Plugboard cycles must only use characters from the characters list.

4. **Settings**
   - `number_of_rotors`: Must match the number of rotor definitions (`r1`, `r2`, etc.).
   - `sequence_of_rotor`: Must specify all rotors in the desired order (e.g., `"r1>r2>r3"`).
   - `iteration`: Non-negative integer, sets the initial step count.
   - `rotation_factor`: Positive integer, controls the stepping logic or 0 for classic enigma stepping mechanism. (Note: Every rotor rotates after moving n steps of the previous rotor, where n is the rotation_factor)

5. **General**
   - All fields are required unless otherwise noted.
   - Validate your configuration using the provided validation functions or by instantiating the Enigma class.

---

## Requirements

- Python 3.7 or newer
- Uses only Python standard libraries: `json`, `logging`, etc.
- No third-party dependencies required

---

## Usage

### Basic Example

```python
from Enigma import Enigma

# Create an Enigma machine instance
enigma = Enigma("configure.json")

# Encode a message
message = "HELLO"
encoded = ""
for char in message:
    encoded += enigma.main(char)
print(f"Encoded: {encoded}")

# Reset the machine to decode
enigma = Enigma("configure.json")
decoded = ""
for char in encoded:
    decoded += enigma.main(char)
print(f"Decoded: {decoded}")
```

---

## Module Contents

### Functions
- `pretest(file)`: Comprehensive configuration validation including rotors, plugs, and characters
- `plug_test(plugs)`: Validate plugboard cycles for repeated characters and conflicts
- `rotor_test(n, rotor)`: Validate rotor wiring as a proper permutation of n character indices

### Classes
- `Enigma`: Main machine controller handling configuration, rotors, plugboard, and encoding
- `Rotor`: Individual rotor with wiring, position tracking, and stepping logic
- `plug`: Plugboard cycle implementation for character swapping/substitution

### Exceptions
- `EnigmaError`: Base exception for all Enigma-related errors
- `ConfigurationError`: Raised for issues with configuration files or data
- `InvalidCharacterError`: Raised when a character is not in the configured character set
- `ValidationError`: Raised when configuration validation fails

---

## Acknowledgments

This project was developed with valuable assistance and contributions from various sources:

### Development Assistance
- **Cursor IDE:** Provided comprehensive code review, documentation assistance, and advanced feature suggestions including type hints, logging, and error handling system design.
- **Windsurf AI (Cascade):** Contributed comprehensive code review, documentation improvements, type hint corrections, character validation enhancements, and error handling throughout the development process.
- **AI Development Tools:** ChatGPT, Claude, Gemini, Perplexity, and DeepSeek provided valuable insights and suggestions during development.
- **Python Community:** Excellent documentation and best practices that guided the implementation and architectural decisions.

### Technical Inspiration
- **Historical Enigma Machine:** The foundational cryptographic principles that inspired this modern implementation.
- **Modern Cryptography Research:** Academic papers and resources on rotor-based encryption systems.

### Tools and Resources
- **Python Standard Library:** For providing robust, dependency-free functionality.
- **GitHub:** For version control and project hosting.
- **Markdown:** For clear, readable documentation formatting.

### Special Thanks
- To the open-source community for promoting knowledge sharing and collaborative development.
- To cryptography researchers and educators who make complex concepts accessible.
- To anyone who tests, uses, or contributes to this project.

If you've contributed to this project in any way and aren't listed here, please let me know so I can add your acknowledgment!

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## Author

Utkarsh(CodeGenixU)

---

## Disclaimer

This project is intended for educational and research purposes only. While it implements advanced cryptographic concepts, it is not recommended for securing sensitive or production data.

## Special Message

This is a special message for mischievous and enthusiastic users & explorers. Even though this project doesn't have any hidden Easter eggs, I encourage you to explore the code, experiment with configurations, and push the boundaries of what this cryptographic machine can do. Your creativity and curiosity are the true keys to unlocking its potential. For experimenting with the code, I recommend keeping some things in mind and following these suggestions for experimentation.

- **Reflector Logic:** You can implement your own reflector logic by creating a new class that inherits from the `Enigma` class and overriding the `main` method to implement your custom logic. While making the new reflector logic, make sure to keep a few points in mind.

    - The reflector logic should be a bijective function in the domain.
    - The reflector logic should have the same domain and range, both from 0 to N-1 where N is the number of characters in the characters list.

- **Rotor Stepping Logic:** You can implement your own rotor logic by creating a new class that inherits from the `Rotor` class and overriding the `__fcode` method to implement your custom logic. While making the new rotor stepping logic, make sure to keep in mind that the stepping logic is properly defined and rotates the rotor.

## Extra Assistance for Special Mischievous Users

- **Reflector Logic**

```python
def main(self, char: str) -> str:
    """Override this method to implement custom reflector logic."""
    if char not in self.characters:
        logger.error(f"Invalid character '{char}' not in character set")
        raise InvalidCharacterError(f"Character '{char}' is not in the configured character set")
    
    logger.debug(f"Processing character: '{char}'")
    
    # Forward pass through plugboard and rotors
    first_encode = self.__plugin(char)
    rotor_encode = self.__prerotor(first_encode)
    for i in self.rotor:
        rotor_encode = self.rotor[i].__fcode(rotor_encode)
    
    # CUSTOM REFLECTOR LOGIC - Replace this line with your implementation
    # Example: reflector = (rotor_encode + 13) % len(self.characters)  # Simple Caesar shift
    # Example: reflector = self.custom_reflection_table[rotor_encode]   # Custom lookup table
    reflector = rotor_encode  # Default: no reflection (placeholder)
    
    # Backward pass through rotors and plugboard
    for i in range(self.number_of_rotors - 1, -1, -1):
        reflector = self.rotor[i].__bcode(reflector)
    rotor_decode = self.__postrotor(reflector)
    final_encode = self.__plugin(rotor_decode, 1)
    self.iteration += 1
    
    logger.debug(f"Encoded '{char}' -> '{final_encode}' (iteration: {self.iteration})")
    return final_encode
```

- **Rotor Logic**

```python
def __fcode(self, n: int) -> int:
    """Override this method to implement custom rotor stepping logic."""
    
    # CUSTOM STEPPING LOGIC - Replace this condition with your implementation
    # Example: if self.iteration % 26 == 0:  # Step every 26 characters
    # Example: if n in self.turnover_positions:  # Step at specific positions
    # Example: if self.should_step():  # Custom stepping function
    if self.iteration % (self.n) ** self.position == 0:  # Default stepping logic
        self.__rotate()
    
    return self.rotor[n]
```

### Usage Instructions

To implement custom logic:

1. **For Custom Reflector Logic**: Create a class that inherits from `Enigma` and override the `main` method using the reflector template above.
2. **For Custom Rotor Stepping**: Create a class that inherits from `Rotor` and override the `__fcode` method using the rotor template above.
3. **For Custom Rotor Stepping**: There is a separate variable rotation_base in the Enigma class and rotation_factor in the Configuration which can be helpful in designing and implementing custom rotor stepping logic without modifying the Configuration.
4. **Important Notes**:
   - Ensure your reflector logic maintains the bijective property (each input maps to exactly one output and each has same domain and range of [0, n - 1] where n is the number of characters in the characters list)
   - Keep rotor stepping logic consistent with your cryptographic requirements
   - Test thoroughly with your specific character set and configuration

**Example Implementation**:
```python
class CustomEnigma(Enigma):
    def main(self, char: str) -> str:
        # Use the reflector template with your custom logic
        pass

class CustomRotor(Rotor):
    def __fcode(self, n: int) -> int:
        # Use the rotor template with your custom stepping logic
        pass
```