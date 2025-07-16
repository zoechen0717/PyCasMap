#!/usr/bin/env python3
"""
Command line interface for PyCasMap
"""

import argparse
import sys
from .core import PyCasMap, SpacerTable, TupleTable, ConstantTable


def main():
    parser = argparse.ArgumentParser(
        description="PyCasMap - Flexible Python CasMap Implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count constructs
  pycasmap constructs -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -c constants.tsv -o output.tsv
  
  # Report spacers
  pycasmap spacers -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv
  
  # Count tuples
  pycasmap tuples -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -o output.tsv
  
  # Build construct sequences
  pycasmap build -s spacers.tsv -c constants.tsv -o constructs.fa
  
  # Describe reads
  pycasmap describe -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -c constants.tsv -o description.tsv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Constructs command
    constructs_parser = subparsers.add_parser('constructs', help='Count perfect constructs')
    constructs_parser.add_argument('-i', '--r1', required=True, help='R1 FASTQ file')
    constructs_parser.add_argument('-I', '--r2', required=True, help='R2 FASTQ file')
    constructs_parser.add_argument('-s', '--spacers', required=True, help='Spacer TSV file')
    constructs_parser.add_argument('-c', '--constants', required=True, help='Constant TSV file')
    constructs_parser.add_argument('-o', '--output', default='construct_counts.tsv', help='Output TSV file')
    
    # Spacers command
    spacers_parser = subparsers.add_parser('spacers', help='Report spacers and counts for each read')
    spacers_parser.add_argument('-i', '--r1', required=True, help='R1 FASTQ file')
    spacers_parser.add_argument('-I', '--r2', required=True, help='R2 FASTQ file')
    spacers_parser.add_argument('-s', '--spacers', required=True, help='Spacer TSV file')
    spacers_parser.add_argument('-o', '--output', default='spacer_counts.tsv', help='Output TSV file')
    
    # Tuples command
    tuples_parser = subparsers.add_parser('tuples', help='Count spacer tuples found')
    tuples_parser.add_argument('-i', '--r1', required=True, help='R1 FASTQ file')
    tuples_parser.add_argument('-I', '--r2', required=True, help='R2 FASTQ file')
    tuples_parser.add_argument('-s', '--spacers', required=True, help='Spacer TSV file')
    tuples_parser.add_argument('-o', '--output', default='tuple_counts.tsv', help='Output TSV file')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build expected construct sequences')
    build_parser.add_argument('-s', '--spacers', required=True, help='Spacer TSV file')
    build_parser.add_argument('-c', '--constants', required=True, help='Constant TSV file')
    build_parser.add_argument('-o', '--output', default='constructs.fa', help='Output FASTA file')
    
    # Describe command
    describe_parser = subparsers.add_parser('describe', help='Describe reads with DRs and spacers')
    describe_parser.add_argument('-i', '--r1', required=True, help='R1 FASTQ file')
    describe_parser.add_argument('-I', '--r2', required=True, help='R2 FASTQ file')
    describe_parser.add_argument('-s', '--spacers', required=True, help='Spacer TSV file')
    describe_parser.add_argument('-c', '--constants', required=True, help='Constant TSV file')
    describe_parser.add_argument('-o', '--output', default='read_description.tsv', help='Output TSV file')
    
    parser.add_argument('-v', '--version', action='version', version='PyCasMap 0.1.0')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize PyCasMap
        pycasmap = PyCasMap()
        
        if args.command == 'constructs':
            # Load data
            print("Loading spacers and constants...")
            spacers = pycasmap.load_spacers(args.spacers)
            constants = pycasmap.load_constants(args.constants)
            
            print(f"Loaded {len(spacers)} spacers and {len(constants)} constants")
            
            # Build constructs
            print("Building constructs...")
            constructs = pycasmap.build_constructs(spacers, constants)
            
            print(f"Built {len(constructs)} constructs")
            if constructs:
                print(f"Plexity range: {min(c.plexity for c in constructs)}-{max(c.plexity for c in constructs)}")
            
            # Process FASTQ files
            print("Processing FASTQ files...")
            counts = pycasmap.process_constructs(args.r1, args.r2)
            
            # Save results
            pycasmap.save_results(counts, args.output)
            
        elif args.command == 'spacers':
            # Load spacers
            print("Loading spacers...")
            spacers = pycasmap.load_spacers(args.spacers)
            spacer_table = SpacerTable(spacers)
            
            print(f"Loaded {len(spacers)} spacers")
            
            # Process FASTQ files
            print("Processing FASTQ files...")
            pycasmap.process_spacers(args.r1, args.r2, spacer_table)
            
        elif args.command == 'tuples':
            # Load spacers
            print("Loading spacers...")
            spacers = pycasmap.load_spacers(args.spacers)
            tuple_table = TupleTable(spacers)
            
            print(f"Loaded {len(spacers)} spacers")
            print(f"Built {tuple_table.len()} tuples")
            
            # Process FASTQ files
            print("Processing FASTQ files...")
            counts = pycasmap.process_tuples(args.r1, args.r2, tuple_table)
            
            # Save results
            pycasmap.save_results(counts, args.output)
            
        elif args.command == 'build':
            # Load data
            print("Loading spacers and constants...")
            spacers = pycasmap.load_spacers(args.spacers)
            constants = pycasmap.load_constants(args.constants)
            
            print(f"Loaded {len(spacers)} spacers and {len(constants)} constants")
            
            # Build constructs
            print("Building constructs...")
            constructs = pycasmap.build_constructs(spacers, constants)
            
            print(f"Built {len(constructs)} constructs")
            
            # Save sequences
            with open(args.output, 'w') as f:
                for construct in constructs:
                    f.write(f">cid_{construct.cid()}\n{construct.sequence()}\n")
            print(f"Construct sequences saved to: {args.output}")
            
        elif args.command == 'describe':
            # Load data
            print("Loading spacers and constants...")
            spacers = pycasmap.load_spacers(args.spacers)
            constants = pycasmap.load_constants(args.constants)
            
            print(f"Loaded {len(spacers)} spacers and {len(constants)} constants")
            
            # Build tables
            tuple_table = TupleTable(spacers)
            constant_table = ConstantTable(constants)
            
            print(f"Built {tuple_table.len()} tuples")
            
            # Process FASTQ files
            print("Processing FASTQ files...")
            pycasmap.describe_reads(args.r1, args.r2, tuple_table, constant_table, args.output)
        
        print("PyCasMap completed successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 