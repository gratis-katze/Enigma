#!/usr/bin/env python3
"""
Main script for the Enigma machine.
Provides command-line interface with proper input validation.
"""

import argparse
import sys
from typing import Optional

# Handle both direct execution and module imports
try:
    from .enigma_machine import EnigmaMachine
    from .config import ROTOR_CONFIGURATIONS, ALPHABET
except ImportError:
    from enigma_machine import EnigmaMachine
    from config import ROTOR_CONFIGURATIONS, ALPHABET


def validate_rotor_types(rotor_types: str) -> list[str]:
    """Validate and parse rotor type string."""
    rotors = rotor_types.split()
    
    if len(rotors) != 3:
        raise ValueError("Exactly 3 rotor types must be specified")
    
    for rotor in rotors:
        if rotor not in ROTOR_CONFIGURATIONS:
            available = ", ".join(ROTOR_CONFIGURATIONS.keys())
            raise ValueError(f"Unknown rotor type '{rotor}'. Available: {available}")
    
    return rotors


def validate_positions(positions: str) -> str:
    """Validate rotor positions string."""
    if len(positions) != 3:
        raise ValueError("Positions must be exactly 3 characters")
    
    positions = positions.upper()
    for pos in positions:
        if pos not in ALPHABET:
            raise ValueError(f"Invalid position '{pos}'. Must be A-Z")
    
    return positions


def interactive_mode() -> None:
    """Run the Enigma machine in interactive mode."""
    print("=== Enigma Machine ===")
    print()
    
    # Get rotor configuration
    available_rotors = ", ".join(ROTOR_CONFIGURATIONS.keys())
    print(f"Available rotor types: {available_rotors}")
    
    while True:
        try:
            rotor_input = input("Enter 3 rotor types (e.g., 'I II III'): ").strip()
            rotors = validate_rotor_types(rotor_input)
            break
        except ValueError as e:
            print(f"Error: {e}")
            continue
    
    # Get initial positions
    while True:
        try:
            positions_input = input("Enter initial positions (e.g., 'MCK'): ").strip()
            positions = validate_positions(positions_input)
            break
        except ValueError as e:
            print(f"Error: {e}")
            continue
    
    # Initialize machine
    try:
        enigma = EnigmaMachine(rotors, positions)
        print(f"\nEnigma machine initialized with rotors {rotors} at positions '{positions}'")
        print("Enter messages to encode/decode (Ctrl+C to exit):")
        print()
        
        while True:
            try:
                message = input("Message: ")
                if not message.strip():
                    continue
                
                result = enigma.encode_message(message)
                
                print(f"Encoded:  {result.encoded_message}")
                print(f"Letters processed: {result.letters_processed}")
                print(f"Rotor steps (L-C-R): {result.rotor_steps}")
                print(f"Final rotor positions: {enigma.get_rotor_positions()}")
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
                
    except Exception as e:
        print(f"Error initializing machine: {e}")
        sys.exit(1)


def batch_mode(rotors: list[str], positions: str, message: str, verbose: bool = False) -> None:
    """Run the Enigma machine in batch mode."""
    try:
        enigma = EnigmaMachine(rotors, positions)
        result = enigma.encode_message(message)
        
        if verbose:
            print(f"Rotors: {rotors}")
            print(f"Initial positions: {positions}")
            print(f"Input message: {message}")
            print(f"Letters processed: {result.letters_processed}")
            print(f"Rotor steps (L-C-R): {result.rotor_steps}")
            print(f"Final rotor positions: {enigma.get_rotor_positions()}")
            print(f"Output: {result.encoded_message}")
        else:
            print(result.encoded_message)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Enigma Machine - Encode/decode messages using historical Enigma cipher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python -m enigmaRevised.main

  Batch mode:
    python -m enigmaRevised.main -r "I II III" -p MCK -m "Hello World"
    
  Verbose output:
    python -m enigmaRevised.main -r "I II III" -p MCK -m "Hello" -v
        """
    )
    
    parser.add_argument(
        '-r', '--rotors',
        help='Rotor types (e.g., "I II III")'
    )
    parser.add_argument(
        '-p', '--positions', 
        help='Initial rotor positions (e.g., "MCK")'
    )
    parser.add_argument(
        '-m', '--message',
        help='Message to encode/decode'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Check if batch mode (all required args provided)
    if args.rotors and args.positions and args.message:
        try:
            rotors = validate_rotor_types(args.rotors)
            positions = validate_positions(args.positions)
            batch_mode(rotors, positions, args.message, args.verbose)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Check for partial batch mode args
    elif any([args.rotors, args.positions, args.message]):
        print("Error: For batch mode, all of --rotors, --positions, and --message are required", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Interactive mode
    else:
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()