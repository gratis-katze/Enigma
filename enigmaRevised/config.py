"""
Configuration data for the Enigma machine components.
Contains rotor wirings, notch positions, and reflector mappings.
"""

# Standard alphabet for position calculations
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Rotor configurations: wiring and notch position
ROTOR_CONFIGURATIONS = {
    "I": {
        "wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "notch": "Q"
    },
    "II": {
        "wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", 
        "notch": "E"
    },
    "III": {
        "wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "notch": "V"
    }
}

# Reflector wiring (B-type reflector)
REFLECTOR_WIRING = "ABCDEFGDIJKGMKMIEBFTCVVJAT"