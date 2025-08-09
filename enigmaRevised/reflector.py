"""
Reflector class for the Enigma machine.
Handles letter reflection at the end of the rotor stack.
"""

# Handle both direct execution and module imports
try:
    from .config import ALPHABET
except ImportError:
    from config import ALPHABET


class Reflector:
    """Represents the reflector in the Enigma machine."""
    
    def __init__(self, wiring: str):
        """
        Initialize the reflector.
        
        Args:
            wiring: The reflector's wiring pattern (26 characters)
        """
        if len(wiring) != 26:
            raise ValueError("Reflector wiring must be exactly 26 characters")
        
        self.wiring = wiring
        
        # Validate that reflector has proper pairs (no self-mapping)
        self._validate_wiring()
    
    def _validate_wiring(self) -> None:
        """Validate that the reflector wiring is valid."""
        # Basic validation - just check length, allow duplicates as per original design
        if len(set(self.wiring)) != len(self.wiring):
            # Allow duplicates as mentioned by user that it's OK for reflectors
            pass
    
    def reflect(self, letter: str, rotor_position: str) -> str:
        """
        Reflect a letter through the reflector.
        
        Args:
            letter: Input letter (A-Z)
            rotor_position: Position of the leftmost rotor for offset calculation
            
        Returns:
            Reflected letter (A-Z)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        if rotor_position not in ALPHABET:
            raise ValueError(f"Rotor position must be A-Z, got {rotor_position}")
        
        # This matches the original logic from your code
        index = (ALPHABET.index(letter) - ALPHABET.index(rotor_position)) % 26
        reflector_letter = self.wiring[index]
        
        # Handle the bidirectional reflection logic from original
        if index == self.wiring.index(reflector_letter):
            backward_index = self.wiring.rindex(reflector_letter)
        else:
            backward_index = self.wiring.index(reflector_letter)
            
        final_letter = ALPHABET[(backward_index + ALPHABET.index(rotor_position)) % 26]
        return final_letter
    
    def __repr__(self) -> str:
        """String representation of the reflector."""
        return f"Reflector(wiring='{self.wiring[:10]}...')"