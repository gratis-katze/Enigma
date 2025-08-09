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
        
        # Initialize rotors (left to right) with rotor types for original algorithm
        self.left_rotor = Rotor(
            ROTOR_CONFIGURATIONS[rotor_types[0]]["wiring"],
            ROTOR_CONFIGURATIONS[rotor_types[0]]["notch"],
            initial_positions[0],
            rotor_types[0]
        )
        self.center_rotor = Rotor(
            ROTOR_CONFIGURATIONS[rotor_types[1]]["wiring"],
            ROTOR_CONFIGURATIONS[rotor_types[1]]["notch"],
            initial_positions[1],
            rotor_types[1]
        )
        self.right_rotor = Rotor(
            ROTOR_CONFIGURATIONS[rotor_types[2]]["wiring"],
            ROTOR_CONFIGURATIONS[rotor_types[2]]["notch"],
            initial_positions[2],
            rotor_types[2]
        )
        
        # Initialize reflector
        self.reflector = Reflector(REFLECTOR_WIRING)
        
        # Store rotor types for original algorithm
        self.rotors = rotor_types
        
        # Step counters for statistics (matching original counters array)
        self.step_counts = [0, 0, 0]  # left, center, right
    
    def _perform_stepping(self) -> None:
        """
        Handle the original stepping logic exactly as it appeared.
        This includes the bugs and duplicate stepping behavior.
        """
        # Always step right rotor first (original behavior)
        self.right_rotor.step()
        
        # Center rotor stepping during encoding (original location of bug)
        if self.center_rotor.is_at_notch():
            self.step_counts[1] += 1  # matches counters[2] in original
            self.center_rotor.step()
            self.left_rotor.step()
        
        # Left rotor stepping during encoding (original location)  
        if self.left_rotor.is_at_notch():
            self.step_counts[0] += 1  # matches counters[3] in original
            self.left_rotor.step()
            
    def _perform_end_stepping(self) -> None:
        """
        Handle the duplicate stepping logic at the end (original bug).
        """
        # Additional stepping check at the end (original duplicate logic bug)
        if self.right_rotor.is_at_notch():
            self.step_counts[1] += 1  # matches counters[1] in original
            self.center_rotor.step()
    
    def encode_letter(self, letter: str) -> str:
        """
        Encode a single letter using the refactored classes with original algorithm.
        
        Each step uses the appropriate class method while maintaining the exact 
        original stepping behavior and encoding sequence.
        
        Args:
            letter: Single letter to encode (A-Z)
            
        Returns:
            Encoded letter (A-Z)
        """
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
        
        current_letter = letter
        
        # Step 1: Always rotate right rotor first (original behavior)
        self.right_rotor.step()
        
        # Step 2: Right rotor encoding (alphabet -> rotor III)
        # Replicates: next_letter(letter, "A", right_position, "ABC", rotors[2])
        current_letter = self.right_rotor.encode_from_alphabet(current_letter, self.right_rotor.position)
        
        # Step 3: Center rotor stepping check DURING encoding (original bug location)
        if self.center_rotor.is_at_notch():
            self.step_counts[1] += 1  # matches counters[2] in original
            self.center_rotor.step()
            self.left_rotor.step()
        
        # Step 4: Center rotor encoding (alphabet -> rotor II)  
        # Replicates: next_letter(letter, right_pos, center_pos, "ABC", rotors[1])
        current_letter = self.right_rotor.encode_through_rotor(
            current_letter, 
            self.right_rotor.position, 
            self.center_rotor.position, 
            self.center_rotor
        )
        
        # Step 5: Left rotor stepping check DURING encoding (original location)
        if self.left_rotor.is_at_notch():
            self.step_counts[0] += 1  # matches counters[3] in original
            self.left_rotor.step()
            
        # Step 6: Left rotor encoding (alphabet -> rotor I)
        # Replicates: next_letter(letter, center_pos, left_pos, "ABC", rotors[0])
        current_letter = self.center_rotor.encode_through_rotor(
            current_letter,
            self.center_rotor.position,
            self.left_rotor.position,
            self.left_rotor
        )
        
        # Step 7: Reflector
        current_letter = self.reflector.reflect(current_letter, self.left_rotor.position)
        
        # Step 8: Backward pass - left rotor (rotor I -> alphabet)
        # Replicates: next_letter(letter, left_pos, center_pos, rotors[0], "ABC")
        current_letter = self.left_rotor.encode_from_rotor(
            current_letter, 
            self.left_rotor.position, 
            self.center_rotor.position, 
            self.left_rotor
        )
        
        # Step 9: Backward pass - center rotor (rotor II -> alphabet)
        # Replicates: next_letter(letter, center_pos, right_pos, rotors[1], "ABC") 
        current_letter = self.center_rotor.encode_from_rotor(
            current_letter,
            self.center_rotor.position,
            self.right_rotor.position,
            self.center_rotor
        )
        
        # Step 10: Backward pass - right rotor (rotor III -> alphabet)
        # Replicates: next_letter(letter, right_pos, "A", rotors[2], "ABC")
        current_letter = self.right_rotor.encode_from_rotor(
            current_letter,
            self.right_rotor.position,
            "A",
            self.right_rotor
        )
        
        # Step 11: Duplicate stepping check at the end (original bug)
        self._perform_end_stepping()
        
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