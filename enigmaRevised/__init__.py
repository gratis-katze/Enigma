"""
Enigma Machine Implementation

A clean, object-oriented implementation of the Enigma machine cipher.
"""

from .enigma_machine import EnigmaMachine, EncodingResult
from .rotor import Rotor
from .reflector import Reflector
from .config import ROTOR_CONFIGURATIONS, ALPHABET

__version__ = "1.0.0"
__all__ = ["EnigmaMachine", "EncodingResult", "Rotor", "Reflector", "ROTOR_CONFIGURATIONS", "ALPHABET"]