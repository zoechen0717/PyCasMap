#!/usr/bin/env python3
"""
Parallel test script for 6plex data to compare casmap and PyCasMap results
"""

import os
import subprocess
import sys
import tempfile

def main():
    spacers_file = "/shen/shenlabstore2/zoechen0717/software/casmap/example_data/casgen_spacers.tsv"
    constants_file = "/shen/shenlabstore2/zoechen0717/software/casmap/example_data/casgen_constants.tsv"
    r1_file = "/shen/shenlabstore2/zoechen0717/software/casmap/example_data/casgen_R1.fastq"
    r2_file = "/shen/shenlabstore2/zoechen0717/software/casmap/example_data/casgen_R2.fastq"
    
    # Check files
    for f in [spacers_file, constants_file, r1_file, r2_file]:
        if not os.path.exists(f):
            print(f"File not found: {f}")
            return 1
    print("All files found!")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
        casmap_output = f.name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
        pycasmap_output = f.name
    
    try:
        # Run casmap
        casmap_cmd = [
            "/shen/shenlabstore2/zoechen0717/software/casmap/target/debug/casmap",
            "constructs",
            "-i", r1_file,
            "-I", r2_file,
            "-s", spacers_file,
            "-c", constants_file,
            "-o", casmap_output
        ]
        print("Running casmap:", ' '.join(casmap_cmd))
        casmap_result = subprocess.run(casmap_cmd, capture_output=True, text=True)
        print(f"casmap exit code: {casmap_result.returncode}")
        if casmap_result.returncode != 0:
            print(casmap_result.stderr)
            return 1
        
        # Run PyCasMap
        pycasmap_cmd = [
            sys.executable, "-m", "pycasmap",
            "constructs",
            "-i", r1_file,
            "-I", r2_file,
            "-s", spacers_file,
            "-c", constants_file,
            "-o", pycasmap_output
        ]
        print("Running PyCasMap:", ' '.join(pycasmap_cmd))
        pycasmap_result = subprocess.run(pycasmap_cmd, capture_output=True, text=True)
        print(f"PyCasMap exit code: {pycasmap_result.returncode}")
        if pycasmap_result.returncode != 0:
            print(pycasmap_result.stderr)
            return 1
        
        # Compare outputs
        print("\nComparing outputs...")
        with open(casmap_output) as f:
            casmap_lines = [line.strip() for line in f if line.strip() and not line.startswith('#') and not line.startswith('ConstructID')]
        with open(pycasmap_output) as f:
            pycasmap_lines = [line.strip() for line in f if line.strip() and not line.startswith('#') and not line.startswith('ConstructID')]
        
        if casmap_lines == pycasmap_lines:
            print("✅ 6plex test PASSED! Outputs are identical.")
        else:
            print("❌ 6plex test FAILED! Outputs differ.")
            print("First 10 lines of casmap output:")
            print('\n'.join(casmap_lines[:10]))
            print("First 10 lines of PyCasMap output:")
            print('\n'.join(pycasmap_lines[:10]))
        return 0
    finally:
        for f in [casmap_output, pycasmap_output]:
            if os.path.exists(f):
                os.unlink(f)

if __name__ == "__main__":
    sys.exit(main()) 