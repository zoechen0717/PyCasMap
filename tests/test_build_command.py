#!/usr/bin/env python3
"""
Test script to compare casmap and PyCasMap build command
"""

import os
import subprocess
import sys
import tempfile

def test_build_command():
    """Test build command comparison"""
    print("Testing build command comparison")
    print("="*50)
    
    # Test data paths
    test_dir = "/shen/shenlabstore2/zoechen0717/1.project/Ruirui"
    spacers_file = os.path.join(test_dir, "test_spacers.tsv")
    constants_file = os.path.join(test_dir, "test_constants.tsv")
    
    # Check if test files exist
    for file_path in [spacers_file, constants_file]:
        if not os.path.exists(file_path):
            print(f"❌ Test file not found: {file_path}")
            assert False, f"Test file not found: {file_path}"
    
    print("✅ All test files found")
    
    # Create temporary output files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fa', delete=False) as f:
        casmap_output = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fa', delete=False) as f:
        pycasmap_output = f.name
    
    try:
        # Run casmap build command
        print("\nRunning casmap build command...")
        casmap_cmd = [
            "/shen/shenlabstore2/zoechen0717/software/casmap/target/debug/casmap",
            "build",
            "-s", spacers_file,
            "-c", constants_file,
            "-o", casmap_output
        ]
        
        casmap_result = subprocess.run(casmap_cmd, capture_output=True, text=True)
        print(f"casmap exit code: {casmap_result.returncode}")
        
        # Run PyCasMap build command
        print("\nRunning PyCasMap build command...")
        pycasmap_cmd = [
            sys.executable, "-m", "pycasmap",
            "build",
            "-s", spacers_file,
            "-c", constants_file,
            "-o", pycasmap_output
        ]
        
        pycasmap_result = subprocess.run(pycasmap_cmd, capture_output=True, text=True)
        print(f"PyCasMap exit code: {pycasmap_result.returncode}")
        
        # Compare results
        print("\n" + "="*30)
        print("COMPARISON")
        print("="*30)
        
        if casmap_result.returncode == 0 and pycasmap_result.returncode == 0:
            print("✅ Both commands completed successfully")
            
            # Read and compare output files
            with open(casmap_output, 'r') as f:
                casmap_content = f.read()
            
            with open(pycasmap_output, 'r') as f:
                pycasmap_content = f.read()
            
            print(f"casmap output length: {len(casmap_content)}")
            print(f"PyCasMap output length: {len(pycasmap_content)}")
            
            # Show first few lines of each
            print("\ncasmap output (first 200 chars):")
            print(casmap_content[:200])
            
            print("\nPyCasMap output (first 200 chars):")
            print(pycasmap_content[:200])
            
            # Check if they're identical
            if casmap_content == pycasmap_content:
                print("\n✅ Output files are IDENTICAL!")
                assert True
            else:
                print("\n❌ Output files differ")
                assert False, "Output files differ"
                
                # Count constructs in each file
                casmap_constructs = casmap_content.count('>cid_')
                pycasmap_constructs = pycasmap_content.count('>cid_')
                print(f"casmap constructs: {casmap_constructs}")
                print(f"PyCasMap constructs: {pycasmap_constructs}")
        else:
            print("❌ One or both commands failed")
            if casmap_result.returncode != 0:
                print(f"casmap error: {casmap_result.stderr}")
            if pycasmap_result.returncode != 0:
                print(f"PyCasMap error: {pycasmap_result.stderr}")
            assert False, "One or both commands failed"
        
    finally:
        # Clean up temporary files
        for file_path in [casmap_output, pycasmap_output]:
            if os.path.exists(file_path):
                os.unlink(file_path)

if __name__ == "__main__":
    test_build_command() 