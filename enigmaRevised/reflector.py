"""
Reflector class for the Enigma machine.
Uses the original reflect algorithm but with clean class structure.
"""

# Handle both direct execution and module imports
try:
    from .config import ALPHABET
except ImportError:
    from config import ALPHABET


class Reflector:
    """
    Represents the reflector in the Enigma machine.
    Encapsulates the original reflect algorithm logic.
    """
    
    def __init__(self, wiring: str):
        """
        Initialize the reflector.
        
        Args:
            wiring: The reflector's wiring pattern (26 characters)
        """
        if len(wiring) != 26:
            raise ValueError("Reflector wiring must be exactly 26 characters")
        
        self.wiring = wiring
        
        # Keep original behavior - no strict validation since duplicates are allowed
        self._validate_wiring()
    
    def _validate_wiring(self) -> None:
        """
        Basic validation of reflector wiring.
        Allows duplicates as per original design requirements.
        """
        # Only validate length - allow duplicates as mentioned by user
        pass
    
    def reflect(self, letter: str, rotor_position: str) -> str:
        """
        Reflect a letter through the reflector using original algorithm.
        
        This exactly replicates the original reflect function:
        - Takes input letter and rotor position  
        - Applies position offset
        - Uses original index/rindex logic for bidirectional reflection
        - Returns position-adjusted output
        
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
        
        # Original algorithm: apply rotor position offset to input
        index = (ALPHABET.index(letter) - ALPHABET.index(rotor_position)) % 26
        
        # Get the letter at this position in reflector wiring
        reflector_letter = self.wiring[index]
        
        # Original bidirectional reflection logic
        # This handles the case where a letter appears multiple times in wiring
        if index == self.wiring.index(reflector_letter):
            # If current index is first occurrence, use last occurrence
            backward_index = self.wiring.rindex(reflector_letter)
        else:
            # Otherwise use first occurrence
            backward_index = self.wiring.index(reflector_letter)
        
        # Apply rotor position offset to output
        final_letter = ALPHABET[(backward_index + ALPHABET.index(rotor_position)) % 26]
        return final_letter
    
    def __repr__(self) -> str:
        """String representation of the reflector."""
        return f"Reflector(wiring='{self.wiring[:10]}...')"