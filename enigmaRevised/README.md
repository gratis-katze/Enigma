# Enigma Machine - Revised Implementation

A clean, object-oriented implementation of the historical Enigma machine cipher used during WWII.

## Features

- **Accurate Historical Simulation**: Implements the 3-rotor Enigma with proper double-stepping mechanism
- **Clean Architecture**: Object-oriented design with separate classes for rotors, reflector, and machine
- **Input Validation**: Comprehensive error checking and validation
- **Flexible Interface**: Both interactive and batch mode operation
- **Case Preservation**: Maintains original case of input text
- **Non-Alphabetic Preservation**: Preserves spaces, punctuation, and numbers
- **Comprehensive Testing**: Full unit test suite

## Architecture

### Files Structure
```
enigmaRevised/
├── __init__.py          # Package initialization
├── config.py            # Rotor and reflector configurations
├── rotor.py             # Rotor class implementation
├── reflector.py         # Reflector class implementation
├── enigma_machine.py    # Main EnigmaMachine class
├── main.py              # Command-line interface
├── test_enigma.py       # Unit tests
└── README.md            # This file
```

### Classes

- **`Rotor`**: Handles individual rotor encoding, stepping, and notch detection
- **`Reflector`**: Manages letter reflection with proper bidirectional mapping
- **`EnigmaMachine`**: Coordinates all components and implements double-stepping
- **`EncodingResult`**: NamedTuple for returning encoding statistics

## Usage

### Interactive Mode
```bash
python -m enigmaRevised.main
```

### Batch Mode
```bash
# Basic usage
python -m enigmaRevised.main -r "I II III" -p "MCK" -m "Hello World"

# Verbose output with statistics
python -m enigmaRevised.main -r "I II III" -p "MCK" -m "Hello World" -v
```

### Programmatic Usage
```python
from enigmaRevised import EnigmaMachine

# Initialize machine
enigma = EnigmaMachine(['I', 'II', 'III'], 'MCK')

# Encode message
result = enigma.encode_message('Hello World')
print(f"Encoded: {result.encoded_message}")
print(f"Letters processed: {result.letters_processed}")
print(f"Rotor steps: {result.rotor_steps}")
```

## Key Improvements Over Original

### 1. **Fixed Critical Bugs**
- ✅ Eliminated duplicate rotor stepping logic
- ✅ Proper double-stepping mechanism implementation
- ✅ Correct stepping order (before encoding)

### 2. **Clean Architecture**
- ✅ Separation of concerns with dedicated classes
- ✅ Configuration separated from logic
- ✅ No global state or variables

### 3. **Robust Error Handling**
- ✅ Input validation for all parameters
- ✅ Descriptive error messages
- ✅ Graceful handling of edge cases

### 4. **Professional Code Quality**
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ PEP 8 compliant code
- ✅ No magic numbers or strings

### 5. **Enhanced Functionality**
- ✅ Both interactive and batch modes
- ✅ Command-line argument parsing
- ✅ Detailed encoding statistics
- ✅ Position reset functionality

### 6. **Testing & Documentation**
- ✅ Complete unit test suite
- ✅ Documentation for all public methods
- ✅ Usage examples and explanations

## Testing

Run the unit tests:
```bash
python -m enigmaRevised.test_enigma
```

## Historical Accuracy

This implementation accurately simulates:
- 3-rotor configuration with historical wirings
- Double-stepping mechanism (the famous "anomaly")
- B-type reflector
- Proper rotor advancement before encoding
- Case preservation and non-alphabetic character handling

## Technical Notes

### Double-Stepping Mechanism
The Enigma machine has a unique double-stepping feature where the center rotor can advance on consecutive key presses under certain conditions. This implementation correctly handles this behavior.

### Reciprocal Property
The Enigma machine is reciprocal - encoding a message twice with the same settings returns the original text. This property is maintained and tested.

### No Self-Encryption
By design, the Enigma machine never encodes a letter as itself, which is maintained through proper rotor and reflector implementation.