"""
Rotor class for the Enigma machine.
Handles rotor rotation, encoding, and notch detection.
"""

# Handle both direct execution and module imports
try:
    from .config import ALPHABET
except ImportError:
    from config import ALPHABET


class Rotor:
    """Represents a single rotor in the Enigma machine."""
    
    def __init__(self, wiring: str, notch: str, position: str = 'A'):
        """
        Initialize a rotor.
        
        Args:
            wiring: The rotor's internal wiring (26 characters)
            notch: The position at which this rotor causes the next rotor to step
            position: Initial position of the rotor (A-Z)
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
    
    def step(self) -> None:
        """Advance the rotor by one position."""
        current_index = ALPHABET.index(self.position)
        self.position = ALPHABET[(current_index + 1) % 26]
    
    def is_at_notch(self) -> bool:
        """Check if the rotor is at its notch position."""
        return self.position == self.notch
    
    def encode_forward(self, letter: str) -> str:
        """
        Encode a letter passing through the rotor from right to left.
        
        Args:
            letter: Input letter (A-Z)
            
        Returns:
            Encoded letter (A-Z)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
            
        # Calculate offset based on rotor position
        offset = ALPHABET.index(self.position)
        
        # Get input position adjusted for rotor position
        input_position = (ALPHABET.index(letter) + offset) % 26
        
        # Get output from rotor wiring
        output_letter = self.wiring[input_position]
        
        # Adjust output for rotor position
        output_position = (ALPHABET.index(output_letter) - offset) % 26
        
        return ALPHABET[output_position]
    
    def encode_backward(self, letter: str) -> str:
        """
        Encode a letter passing through the rotor from left to right (return path).
        
        Args:
            letter: Input letter (A-Z)
            
        Returns:
            Encoded letter (A-Z)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
            
        # Calculate offset based on rotor position
        offset = ALPHABET.index(self.position)
        
        # Adjust input for rotor position
        adjusted_input_position = (ALPHABET.index(letter) + offset) % 26
        adjusted_input_letter = ALPHABET[adjusted_input_position]
        
        # Find where this letter appears in the wiring (reverse lookup)
        wiring_position = self.wiring.index(adjusted_input_letter)
        
        # Adjust output for rotor position
        output_position = (wiring_position - offset) % 26
        
        return ALPHABET[output_position]
    
    def __repr__(self) -> str:
        """String representation of the rotor."""
        return f"Rotor(position='{self.position}', notch='{self.notch}')"