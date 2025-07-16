# PyCasMap Examples

This directory contains example datasets for testing PyCasMap with different plexities (3plex, 4plex, and 6plex).

## Directory Structure

- `3plex/` - 3-plex example with 3 spacers and 3 constants
- `4plex/` - 4-plex example with 4 spacers and 4 constants  
- `6plex/` - 6-plex example with 6 spacers and 6 constants

## File Formats

Each example contains:
- `spacers.txt` - Spacer sequences (one per line)
- `constants.txt` - Constant sequences (one per line)
- `R1.fastq` - R1 FASTQ reads for testing
- `R2.fastq` - R2 FASTQ reads for testing

## Usage Examples

### 4-plex Example
```bash
# Generate constructs
pycasmap constructs examples/4plex/spacers.txt examples/4plex/constants.txt

# Build from FASTQ
pycasmap build examples/4plex/spacers.txt examples/4plex/constants.txt

# Find spacers
pycasmap spacers -i examples/4plex/R1.fastq -I examples/4plex/R2.fastq -s examples/4plex/spacers.txt

# Generate tuples
pycasmap tuples -i examples/4plex/R1.fastq -I examples/4plex/R2.fastq -s examples/4plex/spacers.txt

# Describe constructs
pycasmap describe -i examples/4plex/R1.fastq -I examples/4plex/R2.fastq -s examples/4plex/spacers.txt -c examples/4plex/constants.txt
```

### 6-plex Example
```bash
# Generate constructs
pycasmap constructs -i examples/6plex/R1.fastq -I examples/6plex/R2.fastq -s examples/6plex/spacers.txt -c examples/6plex/constants.txt

# Build from FASTQ
pycasmap build -s examples/6plex/spacers.txt -c examples/6plex/constants.txt
```

### 3-plex Example
```bash
# Generate constructs
pycasmap constructs -i examples/3plex/R1.fastq -I examples/3plex/R2.fastq -s examples/3plex/spacers.txt -c examples/3plex/constants.txt

# Build from FASTQ
pycasmap build -s examples/3plex/spacers.txt -c examples/3plex/constants.txt
```

## Expected Results

- **4-plex**: Even plexity - R1 contains spacers 1,2; R2 contains spacers 3,4 reverse complemented
- **6-plex**: Even plexity - R1 contains spacers 1,2,3; R2 contains spacers 4,5,6 reverse complemented  
- **3-plex**: Odd plexity - R1 contains spacers 1,2; R2 contains spacer 3 reverse complemented 