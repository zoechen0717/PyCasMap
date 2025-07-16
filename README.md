# PyCasMap

**PyCasMap** is a fully compatible Python implementation of the original [casmap](https://github.com/noamteyssier/casmap) tool for CRISPR barcode demultiplexing and quantification. It supports flexible 3-10plex constructs, automatic R1/R2 sequence generation, and produces results identical to the original Rust version.

## Features

- **Full Compatibility**: All main commands (`constructs`, `build`, `spacers`, `tuples`, `describe`) produce results identical to the original casmap (Rust) implementation.
- **Flexible Plexity**: Automatically supports 3-10plex constructs, with correct R1/R2 logic for both even and odd plexity.
- **Automatic R1/R2 Generation**: Strictly follows the original casmap logic for all plexities.
- **Efficient and User-Friendly**: Pure Python, easy to install and extend, with a simple CLI.
- **Extensive Validation**: Parallel tests on 4plex, 6plex, and simulated/real data show 100% agreement with the original casmap.

## Installation

```bash
git clone https://github.com/yourusername/PyCasMap.git
cd PyCasMap
pip install -e .
```

## Quick Start

```bash
pycasmap constructs -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -c constants.tsv -o output.tsv
```

## Input File Formats

### Spacer TSV
```
sequence                cid vid
GATAATGAATCGCATATCGATCC 0   0
TCTAGTAAGTGACATAAGACCGT 0   1
...
```

### Constant TSV
```
sequence         cid
TGACTTTGCCGCATGAGTG 0
GCCACCAAACCAGTTAGAC 1
...
```

## Plexity Logic

- **4plex**: R1 = first 2, R2 = last 2 (reverse complement)
- **6plex**: R1 = first 3, R2 = last 3 (reverse complement)
- **3plex**: R1 = 1,2; R2 = 2,3 (reverse complement)
- **n-plex**: R1 = first n/2, R2 = last n/2 (reverse complement)

## Main Commands

- **Count constructs**:
  ```bash
  pycasmap constructs -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -c constants.tsv -o output.tsv
  ```
- **Build construct FASTA**:
  ```bash
  pycasmap build -s spacers.tsv -c constants.tsv -o constructs.fa
  ```
- **Spacer statistics**:
  ```bash
  pycasmap spacers -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv
  ```
- **Tuple counting**:
  ```bash
  pycasmap tuples -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -o output.tsv
  ```
- **Detailed read description**:
  ```bash
  pycasmap describe -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -c constants.tsv -o description.tsv
  ```

## Output Example

```
ConstructID   Counts
0             1234
1             5678
...
```

## Validation

PyCasMap has been extensively validated against the original casmap using both simulated and real 4plex/6plex data. All main workflows (constructs, build, spacers, tuples) produce **identical results**. See `parallel_test.py` and related scripts for details.

## Contributing

Contributions are welcome! Please fork the repo, create a feature branch, and submit a pull request.

## License

MIT

## Contact

For questions or support, please open an issue on GitHub or contact the maintainer. 