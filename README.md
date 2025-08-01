# Enigma Reloaded

**Beast of an Ancient Legend**

---

This project is not a classic Enigma simulation, but an advanced, extensible cryptographic machine. While its core draws inspiration from the legendary Enigma, this implementation is fundamentally different and vastly more powerful. It features a highly flexible architecture, supporting arbitrary character sets, customizable rotor logic, advanced plugboard cycles, and modern validation and configuration mechanisms.

Enigma Reloaded is designed for cryptographers, researchers, and enthusiasts seeking a customizable, state-of-the-art encryption engine that goes far beyond historical limitations.

## Key Features

- **Highly Configurable Architecture:** Supports any number of rotors, each with fully custom wiring (permutation of indices).
- **Advanced Plugboard System:** Allows multiple variable length disjoint plugboard cycles for additional scrambling.
- **Universal Character Set:** Encode and decode using any set of characters, including Unicode, symbols, and custom alphabets.
- **Modern JSON Configuration:** All settings are loaded from a human-readable JSON file for maximum flexibility.
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

The Enigma machine is configured via a JSON file (see `configure.json` for an example):

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
    "r1": [ ... ],  // Rotor 1 wiring (permutation of indices)
    "r2": [ ... ],  // Rotor 2 wiring
    "r3": [ ... ]   // Rotor 3 wiring
}
```

- **number_of_rotors:** Number of rotors in the machine.
- **sequence_of_rotor:** Order of rotors (e.g., `"r1>r2>r3"`).
- **iteration:** Initial step count for rotor stepping.
- **rotation_factor:** Rotation base (affects stepping).
- **plugs:** List of plugboard cycles (e.g., `["ABCD", "@[{()}]?", "0123456789"]`).
- **characters:** List of all valid characters for encoding.
- **rX:** Each rotor's wiring as a permutation of character indices.

---

## Configuration Rules

When creating or editing your `configure.json` file, follow these rules for correct operation:

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
   - `rotation_factor`: Positive integer, controls the stepping logic.

5. **General**
   - All fields are required unless otherwise noted.
   - Comments are not allowed in standard JSON (remove `//` comments for actual use).
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

- `plug_test(plugs)`: Checks for repeated characters in plugboard cycles.
- `rotor_test(n, rotor)`: Validates rotor wiring as a permutation of n indices.
- `pretest(file)`: Validates configuration file for consistency and correctness.
- `Rotor`: Class representing a single rotor.
- `plug`: Class representing a plugboard cycle.
- `Enigma`: Main class for encoding/decoding using the Enigma machine.

---

## Error Handling

- **ConfigurationError:** Raised for issues with the configuration file.
- **InvalidCharacterError:** Raised if a character is not in the configured character set.
- **ValidationError:** Raised if configuration validation fails.

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## Author

Utkarsh

---

## Disclaimer

This project is intended for educational and research purposes only. While it implements advanced cryptographic concepts, it is not recommended for securing sensitive or production data.
