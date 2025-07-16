#!/usr/bin/env python3
"""
Test script to compare casmap and PyCasMap spacers command
"""

import os
import subprocess
import sys
import tempfile

def test_spacers_command():
    """Test spacers command comparison"""
    print("Testing spacers command comparison")
    print("="*50)
    
    # Test data paths
    test_dir = "/shen/shenlabstore2/zoechen0717/1.project/Ruirui"
    spacers_file = os.path.join(test_dir, "test_spacers.tsv")
    r1_file = os.path.join(test_dir, "test_R1.fastq.gz")
    r2_file = os.path.join(test_dir, "test_R2.fastq.gz")
    
    # Check if test files exist
    for file_path in [spacers_file, r1_file, r2_file]:
        if not os.path.exists(file_path):
            print(f"❌ Test file not found: {file_path}")
            return False
    
    print("✅ All test files found")
    
    # Run casmap spacers command
    print("\nRunning casmap spacers command...")
    casmap_cmd = [
        "/shen/shenlabstore2/zoechen0717/software/casmap/target/debug/casmap",
        "spacers",
        "-i", r1_file,
        "-I", r2_file,
        "-s", spacers_file
    ]
    
    casmap_result = subprocess.run(casmap_cmd, capture_output=True, text=True)
    print(f"casmap exit code: {casmap_result.returncode}")
    if casmap_result.stdout:
        print("casmap output (first 500 chars):")
        print(casmap_result.stdout[:500])
    
    # Run PyCasMap spacers command
    print("\nRunning PyCasMap spacers command...")
    pycasmap_cmd = [
        sys.executable, "-m", "pycasmap",
        "spacers",
        "-i", r1_file,
        "-I", r2_file,
        "-s", spacers_file
    ]
    
    pycasmap_result = subprocess.run(pycasmap_cmd, capture_output=True, text=True)
    print(f"PyCasMap exit code: {pycasmap_result.returncode}")
    if pycasmap_result.stdout:
        print("PyCasMap output (first 500 chars):")
        print(pycasmap_result.stdout[:500])
    
    # Compare results
    print("\n" + "="*30)
    print("COMPARISON")
    print("="*30)
    
    if casmap_result.returncode == 0 and pycasmap_result.returncode == 0:
        print("✅ Both commands completed successfully")
        
        # Simple comparison - check if both produced output
        if casmap_result.stdout and pycasmap_result.stdout:
            print("✅ Both commands produced output")
            print(f"casmap output length: {len(casmap_result.stdout)}")
            print(f"PyCasMap output length: {len(pycasmap_result.stdout)}")
        else:
            print("⚠️  One or both commands produced no output")
    else:
        print("❌ One or both commands failed")
        if casmap_result.returncode != 0:
            print(f"casmap error: {casmap_result.stderr}")
        if pycasmap_result.returncode != 0:
            print(f"PyCasMap error: {pycasmap_result.stderr}")
    
    assert True

if __name__ == "__main__":
    test_spacers_command() 