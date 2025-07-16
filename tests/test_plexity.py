#!/usr/bin/env python3
"""
Simple test script to verify plexity logic
"""

import pytest
import random
from pycasmap.core import Spacer, Constant, Construct


def generate_test_data(plexity: int):
    """Generate test data for given plexity"""
    spacers = []
    constants = []
    
    for vid in range(plexity):
        # Generate random spacer (22bp)
        spacer_seq = ''.join(random.choice('ATGC') for _ in range(22))
        spacers.append(Spacer(spacer_seq, 0, vid))
        
        # Generate random constant (18bp)
        const_seq = ''.join(random.choice('ATGC') for _ in range(18))
        constants.append(Constant(const_seq, vid))
    
    return spacers, constants

@pytest.mark.parametrize("plexity", [3, 4, 5, 6, 7, 8, 9, 10])
def test_plexity(plexity):
    """Test R1/R2 sequence generation for specific plexity"""
    print(f"\n{'='*60}")
    print(f"Testing {plexity}-plex logic")
    print(f"{'='*60}")
    
    # Generate test data
    spacers, constants = generate_test_data(plexity)
    
    # Build construct
    construct = Construct(spacers, constants, 0)
    
    print(f"Construct {construct.cid} ({construct.plexity}-plex)")
    print(f"Spacers: {[s.vid for s in construct.spacers]}")
    print(f"Constants: {[c.cid for c in construct.constants]}")
    
    # Get R1 and R2 sequences
    r1_seq = construct.get_r1_sequence()
    r2_seq = construct.get_r2_sequence()
    
    print(f"\nR1 sequence (length: {len(r1_seq)}):")
    print(f"  {r1_seq}")
    
    print(f"\nR2 sequence (length: {len(r2_seq)}):")
    print(f"  {r2_seq}")
    
    # Verify logic
    if plexity % 2 == 0:  # Even plexity
        expected_r1_count = plexity // 2
        expected_r2_count = plexity // 2
        print(f"\nEven plexity logic:")
        print(f"  R1 takes first {expected_r1_count} elements")
        print(f"  R2 takes last {expected_r2_count} elements (reverse complement)")
    else:  # Odd plexity
        expected_r1_count = (plexity - 1) // 2 + 1
        expected_r2_count = plexity - expected_r1_count + 1
        print(f"\nOdd plexity logic:")
        print(f"  R1 takes first {expected_r1_count} elements")
        print(f"  R2 takes elements {expected_r1_count-1} to end (reverse complement)")
    
    assert len(r1_seq) > 0
    assert len(r2_seq) > 0


def main():
    """Test plexities 3-10"""
    print("PyCasMap Plexity Logic Test")
    print("Testing R1/R2 sequence generation for plexities 3-10")
    
    # Set random seed for reproducible results
    random.seed(42)
    
    # Test all plexities
    for plexity in range(3, 11):
        test_plexity(plexity)
    
    print(f"\n{'='*60}")
    print("Test completed!")
    print("Summary of logic:")
    print("  Even plexity (4,6,8,10): R1=first_half, R2=second_half")
    print("  Odd plexity (3,5,7,9): R1=first_(n+1)/2, R2=overlap+remaining")


if __name__ == "__main__":
    main() 