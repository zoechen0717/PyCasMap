#!/usr/bin/env python3
"""
Parallel test script to compare casmap and PyCasMap results
"""

import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

def run_casmap_constructs(spacers_file, constants_file, r1_file, r2_file, output_file):
    """Run original casmap constructs command"""
    cmd = [
        "/shen/shenlabstore2/zoechen0717/software/casmap/target/debug/casmap",
        "constructs",
        "-i", r1_file,
        "-I", r2_file,
        "-s", spacers_file,
        "-c", constants_file,
        "-o", output_file
    ]
    
    print(f"Running casmap: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"casmap failed: {result.stderr}")
        return False
    
    print(f"casmap completed successfully")
    return True

def run_pycasmap_constructs(spacers_file, constants_file, r1_file, r2_file, output_file):
    """Run PyCasMap constructs command"""
    cmd = [
        sys.executable, "-m", "pycasmap",
        "constructs",
        "-i", r1_file,
        "-I", r2_file,
        "-s", spacers_file,
        "-c", constants_file,
        "-o", output_file
    ]
    
    print(f"Running PyCasMap: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"PyCasMap failed: {result.stderr}")
        return False
    
    print(f"PyCasMap completed successfully")
    return True

def compare_results(casmap_output, pycasmap_output):
    """Compare the results from both tools"""
    print("\n" + "="*60)
    print("COMPARING RESULTS")
    print("="*60)
    
    # Read casmap results
    casmap_results = {}
    try:
        with open(casmap_output, 'r') as f:
            for line in f:
                if line.startswith("ConstructID") or line.startswith("#"):
                    continue
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    cid = int(parts[0])
                    count = int(parts[1])
                    casmap_results[cid] = count
    except Exception as e:
        print(f"Error reading casmap results: {e}")
        return False
    
    # Read PyCasMap results
    pycasmap_results = {}
    try:
        with open(pycasmap_output, 'r') as f:
            for line in f:
                if line.startswith("ConstructID") or line.startswith("#"):
                    continue
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    cid = int(parts[0])
                    count = int(parts[1])
                    pycasmap_results[cid] = count
    except Exception as e:
        print(f"Error reading PyCasMap results: {e}")
        return False
    
    # Compare results
    print(f"casmap found {len(casmap_results)} constructs")
    print(f"PyCasMap found {len(pycasmap_results)} constructs")
    print()
    
    # Check if all construct IDs match
    casmap_cids = set(casmap_results.keys())
    pycasmap_cids = set(pycasmap_results.keys())
    
    if casmap_cids != pycasmap_cids:
        print("❌ Construct IDs don't match!")
        print(f"casmap CIDs: {sorted(casmap_cids)}")
        print(f"PyCasMap CIDs: {sorted(pycasmap_cids)}")
        return False
    
    # Compare counts
    differences = []
    for cid in sorted(casmap_cids):
        casmap_count = casmap_results[cid]
        pycasmap_count = pycasmap_results[cid]
        
        if casmap_count != pycasmap_count:
            differences.append((cid, casmap_count, pycasmap_count))
        else:
            print(f"✅ Construct {cid}: {casmap_count} (both tools agree)")
    
    if differences:
        print("\n❌ COUNT DIFFERENCES FOUND:")
        for cid, casmap_count, pycasmap_count in differences:
            print(f"  Construct {cid}: casmap={casmap_count}, PyCasMap={pycasmap_count}")
        return False
    else:
        print("\n✅ ALL COUNTS MATCH!")
        return True

def main():
    """Main test function"""
    print("PyCasMap vs casmap Parallel Test")
    print("="*50)
    
    # Test data paths
    test_dir = "/shen/shenlabstore2/zoechen0717/1.project/Ruirui"
    spacers_file = os.path.join(test_dir, "test_spacers.tsv")
    constants_file = os.path.join(test_dir, "test_constants.tsv")
    r1_file = os.path.join(test_dir, "test_R1.fastq.gz")
    r2_file = os.path.join(test_dir, "test_R2.fastq.gz")
    
    # Check if test files exist
    for file_path in [spacers_file, constants_file, r1_file, r2_file]:
        if not os.path.exists(file_path):
            print(f"❌ Test file not found: {file_path}")
            return False
    
    print("✅ All test files found")
    
    # Create temporary output files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
        casmap_output = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
        pycasmap_output = f.name
    
    try:
        # Run casmap
        print("\n" + "="*30)
        print("RUNNING CASMAP")
        print("="*30)
        if not run_casmap_constructs(spacers_file, constants_file, r1_file, r2_file, casmap_output):
            return False
        
        # Run PyCasMap
        print("\n" + "="*30)
        print("RUNNING PYCASMAP")
        print("="*30)
        if not run_pycasmap_constructs(spacers_file, constants_file, r1_file, r2_file, pycasmap_output):
            return False
        
        # Compare results
        success = compare_results(casmap_output, pycasmap_output)
        
        if success:
            print("\n🎉 PARALLEL TEST PASSED! PyCasMap and casmap produce identical results!")
        else:
            print("\n💥 PARALLEL TEST FAILED! Results differ between PyCasMap and casmap!")
        
        return success
        
    finally:
        # Clean up temporary files
        for file_path in [casmap_output, pycasmap_output]:
            if os.path.exists(file_path):
                os.unlink(file_path)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 