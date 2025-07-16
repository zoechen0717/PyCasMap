# PyCasMap

**PyCasMap** is a Python tool for constructing and mapping Cas12a-based CRISPR multiplex constructs from high-throughput sequencing data. It supports flexible 3-10plex constructs with automatic R1/R2 sequence generation and produces results identical to the original casmap implementation.

## Features

- **Full Compatibility**: All main commands (`constructs`, `build`, `spacers`, `tuples`, `describe`) produce results identical to the original casmap (Rust) implementation.
- **Flexible Plexity**: Automatically supports 3-10plex constructs, with correct R1/R2 logic for both even and odd plexity.
- **Automatic R1/R2 Generation**: Strictly follows the original casmap logic for all plexities.
- **Efficient and User-Friendly**: Pure Python, easy to install and extend, with a simple CLI.
- **Extensive Validation**: Parallel tests on 4plex, 6plex, and simulated/real data show 100% agreement with the original casmap.

## Installation

```bash
git clone https://github.com/zoechen0717/PyCasMap.git
cd PyCasMap
pip install -e .
```

## Quick Start

```bash
pycasmap constructs -i R1.fastq.gz -I R2.fastq.gz -s spacers.tsv -c constants.tsv -o output.tsv
```

## Input File Formats

### Spacer TSV
Tab-separated file containing spacer sequences with construct ID (cid) and variant ID (vid). Each construct should have the same number of spacers (e.g., 4 for 4-plex, 6 for 6-plex).

```
sequence                cid vid
GATAATGAATCGCATATCGATCC 0   0
TCTAGTAAGTGACATAAGACCGT 0   1
GACCATTGGCTGCGAAGCATCGA 0   2
TTACTCAGTCAGGTGTAACGGTT 0   3
GACAAAACATCCCCATATCTCAC 1   0
CTAACAATGACCTCGATTGCTTG 1   1
GATCCATCCGGAAGCCTATGCTC 1   2
ATCAGTGCTTAACGCGACGCTGG 1   3
```

### Constant TSV
Tab-separated file containing constant sequences (direct repeat regions) with construct ID (cid). The number of constants should match the plexity of your constructs.

```
sequence         cid
TGACTTTGCCGCATGAGTG 0
GCCACCAAACCAGTTAGAC 1
ATGTGGCAATTTGAAAAGG 2
CAGGGGCCGTACCTGAGAT 3
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
## Contributing

Contributions are welcome! Please fork the repo, create a feature branch, and submit a pull request.

## License

MIT

## Contact

For questions or support, please open an issue on GitHub or contact the maintainer. 