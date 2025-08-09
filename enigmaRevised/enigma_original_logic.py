#!/usr/bin/env python3
"""
Exact replica of the original Enigma logic but with clean structure.
This matches the original algorithm precisely to produce identical outputs.
"""

from typing import List, Tuple, NamedTuple

# Handle both direct execution and module imports
try:
    from .config import ROTOR_CONFIGURATIONS, REFLECTOR_WIRING, ALPHABET
except ImportError:
    from config import ROTOR_CONFIGURATIONS, REFLECTOR_WIRING, ALPHABET


class EncodingResult(NamedTuple):
    """Result of encoding a message."""
    encoded_message: str
    letters_processed: int
    rotor_steps: Tuple[int, int, int]  # Steps for left, center, right rotors


class EnigmaOriginalLogic:
    """Enigma machine that exactly replicates the original algorithm."""
    
    def __init__(self, rotor_types: List[str], initial_positions: str):
        """Initialize with original data structures and logic."""
        if len(rotor_types) != 3:
            raise ValueError("Enigma machine requires exactly 3 rotors")
        if len(initial_positions) != 3:
            raise ValueError("Initial positions must be exactly 3 characters")
            
        # Replicate original rotor_dict structure
        self.rotor_dict = {
            "I": [ROTOR_CONFIGURATIONS["I"]["wiring"], ROTOR_CONFIGURATIONS["I"]["notch"]],
            "II": [ROTOR_CONFIGURATIONS["II"]["wiring"], ROTOR_CONFIGURATIONS["II"]["notch"]],
            "III": [ROTOR_CONFIGURATIONS["III"]["wiring"], ROTOR_CONFIGURATIONS["III"]["notch"]],
            "ref": REFLECTOR_WIRING,
            "ABC": [ALPHABET]
        }
        
        # Store rotor types and initial positions
        self.rotors = rotor_types
        self.initial_positions = initial_positions
        
        # Initialize positions (will be reset for each encoding)
        self.reset_positions()
    
    def reset_positions(self):
        """Reset to initial positions."""
        self.rotor_left_position = self.initial_positions[0]
        self.rotor_center_position = self.initial_positions[1]
        self.rotor_right_position = self.initial_positions[2]
        self.counters = [0, 0, 0, 0]  # Matches original
    
    def rotate(self, rotor_position: str) -> str:
        """Exact replica of original rotate function."""
        index = (self.rotor_dict["ABC"][0].index(rotor_position) + 1) % len(self.rotor_dict["ABC"][0])
        rotor_position = self.rotor_dict["ABC"][0][index]
        return rotor_position
    
    def next_letter(self, letter_current: str, rotor_position_current: str, rotor_position_next: str, rotor_current: str, rotor_next: str) -> str:
        """Exact replica of original next_letter function."""
        if rotor_current == "ABC":
            current_wiring = self.rotor_dict["ABC"][0]
        else:
            current_wiring = self.rotor_dict[rotor_current][0]
            
        if rotor_next == "ABC":
            next_wiring = self.rotor_dict["ABC"][0]
        else:
            next_wiring = self.rotor_dict[rotor_next][0]
        
        index = (current_wiring.index(letter_current) - self.rotor_dict["ABC"][0].index(rotor_position_current)) % len(self.rotor_dict["ABC"][0])
        letter_next = next_wiring[(index + self.rotor_dict["ABC"][0].index(rotor_position_next)) % len(self.rotor_dict["ABC"][0])]
        return letter_next
    
    def reflect(self, letter: str, rotor_position: str) -> str:
        """Exact replica of original reflect function."""
        index = (self.rotor_dict["ABC"][0].index(letter) - self.rotor_dict["ABC"][0].index(rotor_position)) % len(self.rotor_dict["ABC"][0])
        reflector_letter = self.rotor_dict["ref"][index]
        if index == self.rotor_dict["ref"].index(reflector_letter):
            backward_index = self.rotor_dict["ref"].rindex(reflector_letter)
        else:
            backward_index = self.rotor_dict["ref"].index(reflector_letter)
        letter = self.rotor_dict["ABC"][0][(backward_index + self.rotor_dict["ABC"][0].index(rotor_position)) % len(self.rotor_dict["ABC"][0])]
        return letter
    
    def encode_letter(self, letter: str) -> str:
        """Exact replica of the original Enigma function logic for one letter."""
        if letter not in ALPHABET:
            raise ValueError(f"Letter must be A-Z, got {letter}")
            
        # Always rotate right rotor (exact match to original)
        self.rotor_right_position = self.rotate(self.rotor_right_position)
        
        # Right rotor encoding
        current_letter = self.next_letter(letter, "A", self.rotor_right_position, "ABC", self.rotors[2])
        
        # Center rotor stepping check (exact match to original)
        if self.rotor_center_position == self.rotor_dict[self.rotors[1]][1]:
            self.counters[2] += 1                
            self.rotor_center_position = self.rotate(self.rotor_center_position)
            self.rotor_left_position = self.rotate(self.rotor_left_position)
        
        # Center rotor encoding
        current_letter = self.next_letter(current_letter, self.rotor_right_position, self.rotor_center_position, "ABC", self.rotors[1])
        
        # Left rotor stepping check (exact match to original)
        if self.rotor_left_position == self.rotor_dict[self.rotors[0]][1]:
            self.counters[3] += 1
            self.rotor_left_position = self.rotate(self.rotor_left_position)
        
        # Left rotor encoding
        current_letter = self.next_letter(current_letter, self.rotor_center_position, self.rotor_left_position, "ABC", self.rotors[0])
        
        # Reflector
        current_letter = self.reflect(current_letter, self.rotor_left_position)
        
        # Backward pass - left rotor
        current_letter = self.next_letter(current_letter, self.rotor_left_position, self.rotor_center_position, self.rotors[0], "ABC")
        
        # Backward pass - center rotor
        current_letter = self.next_letter(current_letter, self.rotor_center_position, self.rotor_right_position, self.rotors[1], "ABC")
        
        # Backward pass - right rotor
        current_letter = self.next_letter(current_letter, self.rotor_right_position, "A", self.rotors[2], "ABC")
        
        # Additional stepping check at the end (exact match to original duplicate logic)
        if self.rotor_right_position == self.rotor_dict[self.rotors[2]][1]:
            self.counters[1] += 1
            self.rotor_center_position = self.rotate(self.rotor_center_position)
        
        return current_letter
    
    def encode_message(self, message: str, preserve_case: bool = True) -> EncodingResult:
        """Encode a complete message using original logic."""
        # Reset to initial positions
        self.reset_positions()
        
        encoded_chars = []
        letters_processed = 0
        
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
            rotor_steps=(self.counters[3], self.counters[2], self.counters[1])  # left, center, right
        )
    
    def get_rotor_positions(self) -> str:
        """Get current rotor positions."""
        return f"{self.rotor_left_position}{self.rotor_center_position}{self.rotor_right_position}"


def main():
    """Test the original logic implementation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enigma Original Logic Test")
    parser.add_argument('-r', '--rotors', default="I II III")
    parser.add_argument('-p', '--positions', default="MCK") 
    parser.add_argument('-m', '--message', default="Hello World")
    parser.add_argument('-v', '--verbose', action='store_true')
    
    args = parser.parse_args()
    
    rotors = args.rotors.split()
    enigma = EnigmaOriginalLogic(rotors, args.positions)
    result = enigma.encode_message(args.message)
    
    if args.verbose:
        print(f"Rotors: {rotors}")
        print(f"Initial positions: {args.positions}")
        print(f"Input message: {args.message}")
        print(f"Letters processed: {result.letters_processed}")
        print(f"Rotor steps (L-C-R): {result.rotor_steps}")
        print(f"Final rotor positions: {enigma.get_rotor_positions()}")
        print(f"Output: {result.encoded_message}")
    else:
        print(result.encoded_message)


if __name__ == "__main__":
    main()