"""
Main Enigma machine implementation.
Coordinates rotors, reflector, and stepping mechanism.
"""

from typing import List, Tuple, NamedTuple

# Handle both direct execution and module imports
try:
    from .rotor import Rotor
    from .reflector import Reflector
    from .config import ROTOR_CONFIGURATIONS, REFLECTOR_WIRING, ALPHABET
except ImportError:
    from rotor import Rotor
    from reflector import Reflector
    from config import ROTOR_CONFIGURATIONS, REFLECTOR_WIRING, ALPHABET


class EncodingResult(NamedTuple):
    """Result of encoding a message."""
    encoded_message: str
    letters_processed: int
    rotor_steps: Tuple[int, int, int]  # Steps for left, center, right rotors


class EnigmaMachine:
    """Complete Enigma machine with three rotors and a reflector."""
    
    def __init__(self, rotor_types: List[str], initial_positions: str):
        """
        Initialize the Enigma machine.
        
        Args:
            rotor_types: List of rotor type names (e.g., ['I', 'II', 'III'])
            initial_positions: Initial rotor positions as string (e.g., 'MCK')
        """
        if len(rotor_types) != 3:
            raise ValueError("Enigma machine requires exactly 3 rotors")
        if len(initial_positions) != 3:
            raise ValueError("Initial positions must be exactly 3 characters")
            
        # Validate rotor types exist
        for rotor_type in rotor_types:
            if rotor_type not in ROTOR_CONFIGURATIONS:
                raise ValueError(f"Unknown rotor type: {rotor_type}")
        
        # Validate positions
        for pos in initial_positions:
            if pos not in ALPHABET:
                raise ValueError(f"Invalid position: {pos}")
        
        # Initialize rotors (left to right)
        self.left_rotor = Rotor(
            ROTOR_CONFIGURATIONS[rotor_types[0]]["wiring"],
            ROTOR_CONFIGURATIONS[rotor_types[0]]["notch"],
            initial_positions[0]
        )
        self.center_rotor = Rotor(
            ROTOR_CONFIGURATIONS[rotor_types[1]]["wiring"],
            ROTOR_CONFIGURATIONS[rotor_types[1]]["notch"],
            initial_positions[1]
        )
        self.right_rotor = Rotor(
            ROTOR_CONFIGURATIONS[rotor_types[2]]["wiring"],
            ROTOR_CONFIGURATIONS[rotor_types[2]]["notch"],
            initial_positions[2]
        )
        
        # Initialize reflector
        self.reflector = Reflector(REFLECTOR_WIRING)
        
        # Step counters for statistics
        self.step_counts = [0, 0, 0]  # left, center, right
    
    def _step_rotors(self) -> None:
        """
        Handle rotor stepping according to Enigma double-stepping mechanism.
        This must be called BEFORE encoding each letter.
        """
        # Check for double-stepping condition
        center_at_notch = self.center_rotor.is_at_notch()
        right_at_notch = self.right_rotor.is_at_notch()
        
        # Always step the right rotor
        self.right_rotor.step()
        self.step_counts[2] += 1
        
        # Step center rotor if right rotor was at notch or center rotor is at notch (double-stepping)
        if right_at_notch or center_at_notch:
            self.center_rotor.step()
            self.step_counts[1] += 1
        
        # Step left rotor if center rotor was at notch
        if center_at_notch:
            self.left_rotor.step()
            self.step_counts[0] += 1
    
    def encode_letter(self, letter: str) -> str:
        """
        Encode a single letter through the complete Enigma mechanism.
        This replicates the exact logic from the original implementation.
        
        Args:
            letter: Single letter to encode (A-Z)
            
        Returns:
            Encoded letter (A-Z)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        
        # Always rotate right rotor first (matches original)
        self.right_rotor.step()
        self.step_counts[2] += 1
        
        # Forward pass through rotors (right to left)
        current_letter = letter
        
        # Right rotor encoding
        current_letter = self.right_rotor.encode_forward(current_letter)
        
        # Center rotor - check for stepping DURING encoding (matches original)
        if self.center_rotor.is_at_notch():
            self.center_rotor.step()
            self.left_rotor.step()
            self.step_counts[1] += 1
            self.step_counts[0] += 1
            
        current_letter = self.center_rotor.encode_forward(current_letter)
        
        # Left rotor - check for stepping DURING encoding (matches original)
        if self.left_rotor.is_at_notch():
            self.left_rotor.step()
            self.step_counts[0] += 1
            
        current_letter = self.left_rotor.encode_forward(current_letter)
        
        # Reflection
        current_letter = self.reflector.reflect(current_letter, self.left_rotor.position)
        
        # Backward pass through rotors (left to right)
        current_letter = self.left_rotor.encode_backward(current_letter)
        current_letter = self.center_rotor.encode_backward(current_letter)
        current_letter = self.right_rotor.encode_backward(current_letter)
        
        # Additional stepping check at the end (matches original duplicate logic)
        if self.right_rotor.is_at_notch():
            self.center_rotor.step()
            self.step_counts[1] += 1
        
        return current_letter
    
    def encode_message(self, message: str, preserve_case: bool = True) -> EncodingResult:
        """
        Encode a complete message.
        
        Args:
            message: Input message
            preserve_case: Whether to preserve original case of letters
            
        Returns:
            EncodingResult with encoded message and statistics
        """
        encoded_chars = []
        letters_processed = 0
        
        # Reset step counters
        self.step_counts = [0, 0, 0]
        
        for char in message:
            if char.isalpha():
                # Track original case
                was_lowercase = char.islower()
                
                # Encode uppercase letter
                encoded_char = self.encode_letter(char.upper())
                
                # Restore case if requested
                if preserve_case and was_lowercase:
                    encoded_char = encoded_char.lower()
                
                encoded_chars.append(encoded_char)
                letters_processed += 1
            else:
                # Preserve non-alphabetic characters
                encoded_chars.append(char)
        
        return EncodingResult(
            encoded_message=''.join(encoded_chars),
            letters_processed=letters_processed,
            rotor_steps=tuple(self.step_counts)
        )
    
    def get_rotor_positions(self) -> str:
        """Get current positions of all rotors."""
        return f"{self.left_rotor.position}{self.center_rotor.position}{self.right_rotor.position}"
    
    def reset_to_positions(self, positions: str) -> None:
        """Reset rotors to specific positions."""
        if len(positions) != 3:
            raise ValueError("Positions must be exactly 3 characters")
        
        for pos in positions:
            if pos not in ALPHABET:
                raise ValueError(f"Invalid position: {pos}")
        
        self.left_rotor.position = positions[0]
        self.center_rotor.position = positions[1] 
        self.right_rotor.position = positions[2]
        
        # Reset step counters
        self.step_counts = [0, 0, 0]
    
    def __repr__(self) -> str:
        """String representation of the machine."""
        return f"EnigmaMachine(positions='{self.get_rotor_positions()}')"