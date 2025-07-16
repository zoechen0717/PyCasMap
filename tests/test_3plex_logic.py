#!/usr/bin/env python3
"""
Test script to verify 3-plex R1/R2 generation logic
"""

from pycasmap.core import Spacer, Constant, Construct

def reverse_complement(sequence: str) -> str:
    """Generate reverse complement of sequence"""
    complement = str.maketrans('ATGCatgc', 'TACGtacg')
    return sequence.translate(complement)[::-1]

def test_3plex_logic():
    """Test 3-plex construct generation"""
    print("Testing 3-plex R1/R2 generation logic")
    print("=" * 50)
    
    # Create test spacers for 3-plex construct
    spacers = [
        Spacer("SPACER1", 0, 0),  # First spacer
        Spacer("SPACER2", 0, 1),  # Second spacer  
        Spacer("SPACER3", 0, 2),  # Third spacer
    ]
    
    # Create test constants
    constants = [
        Constant("CONST1", 0),  # First constant
        Constant("CONST2", 0),  # Second constant
        Constant("CONST3", 0),  # Third constant
    ]
    
    # Create 3-plex construct
    construct = Construct(spacers, constants, 0)
    
    print(f"Construct ID: {construct.cid}")
    print(f"Plexity: {construct.plexity}")
    print(f"Full sequence: {construct.sequence()}")
    print()
    
    # Generate R1 and R2 sequences
    r1_seq = construct.get_r1_sequence()
    r2_seq = construct.get_r2_sequence()
    
    print("R1 sequence (should contain spacer1, spacer2):")
    print(f"  {r1_seq}")
    print()
    
    print("R2 sequence (should contain spacer2, spacer3, reverse complement):")
    print(f"  {r2_seq}")
    print()
    
    # Get the original R2 sequence before reverse complement
    r2_original = reverse_complement(r2_seq)
    print("R2 original sequence (before reverse complement):")
    print(f"  {r2_original}")
    print()
    
    # Verify the logic
    print("Verification:")
    print(f"  R1 contains SPACER1: {'SPACER1' in r1_seq}")
    print(f"  R1 contains SPACER2: {'SPACER2' in r1_seq}")
    print(f"  R1 contains SPACER3: {'SPACER3' in r1_seq}")
    print()
    print(f"  R2 original contains SPACER1: {'SPACER1' in r2_original}")
    print(f"  R2 original contains SPACER2: {'SPACER2' in r2_original}")
    print(f"  R2 original contains SPACER3: {'SPACER3' in r2_original}")
    print()
    
    # Check if R1 has spacers 1,2 and R2 has spacers 2,3
    r1_has_1_2 = 'SPACER1' in r1_seq and 'SPACER2' in r1_seq and 'SPACER3' not in r1_seq
    r2_has_2_3 = 'SPACER2' in r2_original and 'SPACER3' in r2_original and 'SPACER1' not in r2_original
    
    print("Expected logic verification:")
    print(f"  R1 contains spacers 1,2 only: {r1_has_1_2}")
    print(f"  R2 contains spacers 2,3 only: {r2_has_2_3}")
    print()
    
    assert r1_has_1_2 and r2_has_2_3

if __name__ == "__main__":
    test_3plex_logic() 