"""
Rotor class for the Enigma machine.
Uses the original algorithm logic but with clean class structure.
"""

# Handle both direct execution and module imports
try:
    from .config import ALPHABET
except ImportError:
    from config import ALPHABET


class Rotor:
    """
    Represents a single rotor in the Enigma machine.
    Implements the original next_letter algorithm logic internally.
    """
    
    def __init__(self, wiring: str, notch: str, position: str = 'A', rotor_type: str = ""):
        """
        Initialize a rotor.
        
        Args:
            wiring: The rotor's internal wiring (26 characters)
            notch: The position at which this rotor causes the next rotor to step
            position: Initial position of the rotor (A-Z)
            rotor_type: The rotor type name (e.g., 'I', 'II', 'III') for original algorithm
        """
        if len(wiring) != 26:
            raise ValueError("Rotor wiring must be exactly 26 characters")
        if position not in ALPHABET:
            raise ValueError(f"Position must be A-Z, got {position}")
        if notch not in ALPHABET:
            raise ValueError(f"Notch must be A-Z, got {notch}")
            
        self.wiring = wiring
        self.notch = notch
        self.position = position
        self.rotor_type = rotor_type
    
    def step(self) -> None:
        """
        Advance the rotor by one position using original rotate logic.
        """
        current_index = ALPHABET.index(self.position)
        self.position = ALPHABET[(current_index + 1) % 26]
    
    def is_at_notch(self) -> bool:
        """Check if the rotor is at its notch position."""
        return self.position == self.notch
    
    def encode_from_alphabet(self, letter: str, output_position: str) -> str:
        """
        Encode letter from alphabet through rotor (original algorithm).
        Replicates: next_letter(letter, "A", rotor_position, "ABC", rotor_type)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        if output_position not in ALPHABET:
            raise ValueError(f"Output position must be A-Z, got {output_position}")
            
        # Original algorithm math: from alphabet wiring through rotor
        index = (ALPHABET.index(letter) - ALPHABET.index("A")) % 26
        encoded_letter = self.wiring[(index + ALPHABET.index(output_position)) % 26]
        return encoded_letter
    
    def encode_to_alphabet(self, letter: str, input_position: str) -> str:
        """
        Encode letter from rotor to alphabet (original algorithm).
        Replicates: next_letter(letter, rotor_position, "A", rotor_type, "ABC")
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        if input_position not in ALPHABET:
            raise ValueError(f"Input position must be A-Z, got {input_position}")
            
        # Original algorithm math: from rotor wiring to alphabet
        index = (self.wiring.index(letter) - ALPHABET.index(input_position)) % 26
        encoded_letter = ALPHABET[(index + ALPHABET.index("A")) % 26]
        return encoded_letter
    
    def encode_through_rotor(self, letter: str, input_position: str, output_position: str, target_rotor) -> str:
        """
        Encode letter from this rotor through another rotor (original algorithm).
        Replicates: next_letter(letter, input_pos, output_pos, "ABC", target_rotor_type)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        if input_position not in ALPHABET:
            raise ValueError(f"Input position must be A-Z, got {input_position}")
        if output_position not in ALPHABET:
            raise ValueError(f"Output position must be A-Z, got {output_position}")
            
        # Original algorithm math: from alphabet through target rotor
        index = (ALPHABET.index(letter) - ALPHABET.index(input_position)) % 26
        encoded_letter = target_rotor.wiring[(index + ALPHABET.index(output_position)) % 26]
        return encoded_letter
    
    def encode_from_rotor(self, letter: str, input_position: str, output_position: str, source_rotor) -> str:
        """
        Encode letter from another rotor through alphabet (original algorithm).
        Replicates: next_letter(letter, input_pos, output_pos, source_rotor_type, "ABC")
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        if input_position not in ALPHABET:
            raise ValueError(f"Input position must be A-Z, got {input_position}")
        if output_position not in ALPHABET:
            raise ValueError(f"Output position must be A-Z, got {output_position}")
            
        # Original algorithm math: from source rotor to alphabet
        index = (source_rotor.wiring.index(letter) - ALPHABET.index(input_position)) % 26
        encoded_letter = ALPHABET[(index + ALPHABET.index(output_position)) % 26]
        return encoded_letter
    
    def __repr__(self) -> str:
        """String representation of the rotor."""
        return f"Rotor(type='{self.rotor_type}', position='{self.position}', notch='{self.notch}')"