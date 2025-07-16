"""
Core PyCasMap functionality - Complete implementation of all casmap features
"""

import gzip
import csv
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional
import itertools


class Spacer:
    """Represents a spacer sequence with construct and variant IDs"""
    
    def __init__(self, sequence: str, cid: int, vid: int):
        self.sequence = sequence
        self.cid = cid
        self.vid = vid
    
    def __repr__(self):
        return f"Spacer(seq='{self.sequence}', cid={self.cid}, vid={self.vid})"


class Constant:
    """Represents a constant sequence with ID"""
    
    def __init__(self, sequence: str, cid: int):
        self.sequence = sequence
        self.cid = cid
    
    def __repr__(self):
        return f"Constant(seq='{self.sequence}', cid={self.cid})"


class Construct:
    """Represents a complete construct with spacers and constants"""
    
    def __init__(self, spacers: List[Spacer], constants: List[Constant], construct_id: int):
        self.spacers = spacers
        self.constants = constants
        self.construct_id = construct_id
        self.plexity = len(spacers)
    
    def get_r1_sequence(self) -> str:
        """Generate R1 sequence based on plexity - matches original casmap logic"""
        if self.plexity == 4:
            # For 4-plex: take first 2 spacers and constants
            take_count = 2
        elif self.plexity == 6:
            # For 6-plex: take first 3 spacers and constants
            take_count = 3
        elif self.plexity == 3:
            # For 3-plex: take first 2 spacers and constants (1,2)
            take_count = 2
        else:
            # For other plexities: take first half
            take_count = self.plexity // 2
        
        s_iter = self.spacers[:take_count]
        c_iter = self.constants[:take_count]
        seq = ""
        for const, spacer in zip(c_iter, s_iter):
            seq += const.sequence + spacer.sequence
        return seq
    
    def get_r2_sequence(self) -> str:
        """Generate R2 sequence based on plexity (reverse complement) - matches original casmap logic"""
        if self.plexity == 4:
            # For 4-plex: take last 2 spacers and constants, reverse complement
            take_count = 2
            s_iter = self.spacers[-take_count:]
            c_iter = self.constants[-take_count:]
        elif self.plexity == 6:
            # For 6-plex: take last 3 spacers and constants, reverse complement
            take_count = 3
            s_iter = self.spacers[-take_count:]
            c_iter = self.constants[-take_count:]
        elif self.plexity == 3:
            # For 3-plex: take last 2 spacers and constants (2,3), reverse complement
            take_count = 2
            s_iter = self.spacers[-take_count:]
            c_iter = self.constants[-take_count:]
        else:
            # For other plexities: take second half
            take_count = self.plexity // 2
            start_idx = self.plexity - take_count
            s_iter = self.spacers[start_idx:]
            c_iter = self.constants[start_idx:]
        
        seq = ""
        for const, spacer in zip(c_iter, s_iter):
            seq += const.sequence + spacer.sequence
        
        return self._reverse_complement(seq)
    
    def _build_sequence(self, spacers: List[Spacer], constants: List[Constant]) -> str:
        """Build sequence by alternating constants and spacers"""
        seq = ""
        for const, spacer in zip(constants, spacers):
            seq += const.sequence + spacer.sequence
        return seq
    
    def _reverse_complement(self, sequence: str) -> str:
        """Generate reverse complement of sequence"""
        complement = str.maketrans('ATGCatgc', 'TACGtacg')
        return sequence.translate(complement)[::-1]
    
    def sequence(self) -> str:
        """Get full construct sequence"""
        return self._build_sequence(self.spacers, self.constants)
    
    @property
    def cid(self) -> int:
        """Get construct ID"""
        return self.construct_id


class KmerIter:
    """Iterator for k-mers in a sequence"""
    
    def __init__(self, sequence: str, k: int):
        self.sequence = sequence
        self.k = k
        self.pos = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.pos + self.k > len(self.sequence):
            raise StopIteration
        kmer = self.sequence[self.pos:self.pos + self.k]
        self.pos += 1
        return kmer


class SpacerTable:
    """Table for spacer matching"""
    
    def __init__(self, spacers: List[Spacer]):
        self.spacers = spacers
        self.spacer_set = {spacer.sequence for spacer in spacers}
        self._spacer_length = len(spacers[0].sequence) if spacers else 0
    
    def contains(self, sequence: str) -> Optional[str]:
        """Check if sequence contains a spacer"""
        if sequence in self.spacer_set:
            return sequence
        return None
    
    def spacer_length(self) -> int:
        """Get spacer length"""
        return self._spacer_length


class TupleTable:
    """Table for tuple matching (4-plex and 6-plex)"""
    
    def __init__(self, spacers: List[Spacer]):
        self.spacers = spacers
        self.spacer_set = {spacer.sequence for spacer in spacers}
        self._spacer_length = len(spacers[0].sequence) if spacers else 0
        
        # Group spacers by construct ID
        spacer_groups = defaultdict(list)
        for spacer in spacers:
            spacer_groups[spacer.cid].append(spacer)
        
        # Determine spacer count per construct
        if not spacer_groups:
            self.spacer_count = 0
        else:
            first_group = list(spacer_groups.values())[0]
            self.spacer_count = len(first_group)
        
        # Build tuple maps
        self.tuple_map_4 = {}
        self.tuple_map_6 = {}
        
        for cid, spacer_group in spacer_groups.items():
            spacer_group.sort(key=lambda x: x.vid)
            sequences = [spacer.sequence for spacer in spacer_group]
            
            if self.spacer_count == 4:
                tuple_4 = tuple(sequences[:4])
                self.tuple_map_4[tuple_4] = cid
            elif self.spacer_count == 6:
                tuple_6 = tuple(sequences[:6])
                self.tuple_map_6[tuple_6] = cid
    
    def get_spacer(self, sequence: str) -> Optional[str]:
        """Get spacer sequence if it exists"""
        if sequence in self.spacer_set:
            return sequence
        return None
    
    def get_tuple_4(self, tuple_4: Tuple[str, str, str, str]) -> Optional[int]:
        """Get construct ID for 4-tuple"""
        return self.tuple_map_4.get(tuple_4)
    
    def get_tuple_6(self, tuple_6: Tuple[str, str, str, str, str, str]) -> Optional[int]:
        """Get construct ID for 6-tuple"""
        return self.tuple_map_6.get(tuple_6)
    
    def k(self) -> int:
        """Get spacer length"""
        return self._spacer_length
    
    def len(self) -> int:
        """Get number of constructs"""
        if self.spacer_count == 4:
            return len(self.tuple_map_4)
        else:
            return len(self.tuple_map_6)


class ConstantTable:
    """Table for constant matching"""
    
    def __init__(self, constants: List[Constant]):
        self.constants = constants
        self.constant_map = {constant.sequence: constant for constant in constants}
        self._k = len(constants[0].sequence) if constants else 0
    
    def get_constant(self, sequence: str) -> Optional[Constant]:
        """Get constant if it exists"""
        return self.constant_map.get(sequence)
    
    def k(self) -> int:
        """Get constant length"""
        return self._k


class PyCasMap:
    """Main PyCasMap class for processing constructs"""
    
    def __init__(self):
        self.constructs: List[Construct] = []
        self.r1_table: Dict[str, Set[int]] = defaultdict(set)
        self.r2_table: Dict[str, Set[int]] = defaultdict(set)
    
    def load_spacers(self, filename: str) -> List[Spacer]:
        """Load spacers from TSV file"""
        spacers = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) >= 3:
                    sequence, cid, vid = row[0], int(row[1]), int(row[2])
                    spacers.append(Spacer(sequence, cid, vid))
        return sorted(spacers, key=lambda x: (x.cid, x.vid))
    
    def load_constants(self, filename: str) -> List[Constant]:
        """Load constants from TSV file"""
        constants = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) >= 2:
                    sequence, cid = row[0], int(row[1])
                    constants.append(Constant(sequence, cid))
        return sorted(constants, key=lambda x: x.cid)
    
    def build_constructs(self, spacers: List[Spacer], constants: List[Constant]) -> List[Construct]:
        """Build constructs from spacers and constants - matches original casmap logic"""
        constructs = []
        
        # Determine spacer count per construct by checking the first few spacers
        spacer_count = 0
        if len(spacers) >= 6 and spacers[0].cid == spacers[1].cid and spacers[1].cid == spacers[2].cid and \
           spacers[2].cid == spacers[3].cid and spacers[3].cid == spacers[4].cid and spacers[4].cid == spacers[5].cid:
            spacer_count = 6
        elif len(spacers) >= 4 and spacers[0].cid == spacers[1].cid and spacers[1].cid == spacers[2].cid and \
             spacers[2].cid == spacers[3].cid:
            spacer_count = 4
        else:
            raise ValueError("Unable to determine spacer count per construct. Expected 4 or 6 spacers per construct.")
        
        # Build constructs by chunks
        for cid, chunk in enumerate(spacers[::spacer_count]):
            if cid * spacer_count + spacer_count <= len(spacers):
                spacer_chunk = spacers[cid * spacer_count:(cid + 1) * spacer_count]
                construct = Construct(spacer_chunk, constants, cid)
                constructs.append(construct)
                
                # Build hash tables for fast lookup
                r1_seq = construct.get_r1_sequence()
                r2_seq = construct.get_r2_sequence()
                
                self.r1_table[r1_seq].add(cid)
                self.r2_table[r2_seq].add(cid)
                
                print(f"Debug: Construct {cid} ({construct.plexity}-plex)")
                print(f"  R1: {r1_seq} (length: {len(r1_seq)})")
                print(f"  R2: {r2_seq} (length: {len(r2_seq)})")
        
        return constructs
    
    def process_constructs(self, r1_file: str, r2_file: str) -> Dict[int, int]:
        """Process paired FASTQ files and count constructs - matches original casmap logic"""
        counts = defaultdict(int)
        total_reads = 0
        mapped_reads = 0
        
        # Open FASTQ files
        r1_opener = gzip.open if r1_file.endswith('.gz') else open
        r2_opener = gzip.open if r2_file.endswith('.gz') else open
        
        with r1_opener(r1_file, 'rt') as r1_f, r2_opener(r2_file, 'rt') as r2_f:
            for r1_bytes, r2_bytes in zip(r1_f, r2_f):
                total_reads += 1
                
                # Get sequence lines (every 4th line starting from line 1)
                if total_reads % 4 == 1:  # Header line
                    continue
                elif total_reads % 4 == 2:  # Sequence line
                    r1_seq = r1_bytes.strip()
                    r2_seq = r2_bytes.strip()
                    
                    # Find matching construct
                    matched_cid = self._find_matching_construct(r1_seq, r2_seq)
                    if matched_cid is not None:
                        counts[matched_cid] += 1
                        mapped_reads += 1
                
                # Skip quality lines
                elif total_reads % 4 == 3:  # Plus line
                    continue
                elif total_reads % 4 == 0:  # Quality line
                    continue
        
        print(f"Total reads processed: {total_reads // 4}")
        print(f"Mapped reads: {mapped_reads}")
        print(f"Mapping rate: {mapped_reads / (total_reads // 4):.4f}")
        
        return counts
    
    def process_spacers(self, r1_file: str, r2_file: str, spacer_table: SpacerTable) -> None:
        """Process FASTQ files and report spacers found in each read - matches original casmap logic"""
        r1_opener = gzip.open if r1_file.endswith('.gz') else open
        r2_opener = gzip.open if r2_file.endswith('.gz') else open
        
        with r1_opener(r1_file, 'rt') as r1_f, r2_opener(r2_file, 'rt') as r2_f:
            for r1_bytes, r2_bytes in zip(r1_f, r2_f):
                # Get sequence lines
                if r1_bytes.startswith('@'):  # Header
                    continue
                elif r1_bytes.startswith('+'):  # Plus line
                    continue
                elif r1_bytes.startswith('!'):  # Quality line
                    continue
                else:  # Sequence line
                    r1_seq = r1_bytes.strip()
                    r2_seq = r2_bytes.strip()
                    
                    # Find spacers in R1 and R2
                    r1_spacers = self._find_spacers(r1_seq, spacer_table)
                    r2_spacers = self._find_spacers(r2_seq, spacer_table)
                    
                    # Combine and count
                    all_spacers = r1_spacers + r2_spacers
                    spacer_counts = defaultdict(int)
                    for spacer in all_spacers:
                        spacer_counts[spacer] += 1
                    
                    print(f"Spacers found: {dict(spacer_counts)}")
    
    def process_tuples(self, r1_file: str, r2_file: str, tuple_table: TupleTable) -> Dict[int, int]:
        """Process FASTQ files and count tuples - matches original casmap logic"""
        counts = defaultdict(int)
        total_reads = 0
        mapped_reads = 0
        
        r1_opener = gzip.open if r1_file.endswith('.gz') else open
        r2_opener = gzip.open if r2_file.endswith('.gz') else open
        
        with r1_opener(r1_file, 'rt') as r1_f, r2_opener(r2_file, 'rt') as r2_f:
            for r1_bytes, r2_bytes in zip(r1_f, r2_f):
                total_reads += 1
                
                if total_reads % 4 == 1:  # Header line
                    continue
                elif total_reads % 4 == 2:  # Sequence line
                    r1_seq = r1_bytes.strip()
                    r2_seq = r2_bytes.strip()
                    
                    # Find matching tuple
                    matched_cid = self._find_matching_tuple(r1_seq, r2_seq, tuple_table)
                    if matched_cid is not None:
                        counts[matched_cid] += 1
                        mapped_reads += 1
                
                elif total_reads % 4 == 3:  # Plus line
                    continue
                elif total_reads % 4 == 0:  # Quality line
                    continue
        
        print(f"Total reads processed: {total_reads // 4}")
        print(f"Mapped reads: {mapped_reads}")
        print(f"Mapping rate: {mapped_reads / (total_reads // 4):.4f}")
        
        return counts
    
    def build_construct_sequences(self, output_file: str) -> None:
        """Build and save construct sequences to FASTA file"""
        with open(output_file, 'w') as f:
            for construct in self.constructs:
                f.write(f">cid_{construct.cid}\n{construct.sequence()}\n")
        print(f"Construct sequences saved to: {output_file}")
    
    def describe_reads(self, r1_file: str, r2_file: str, tuple_table: TupleTable, 
                      constant_table: ConstantTable, output_file: str) -> None:
        """Describe reads with found DRs and spacers - matches original casmap logic"""
        with open(output_file, 'w') as f:
            # Write header
            fields = ["index", "dr1", "dr2", "dr3", "spacer1", "spacer2", "spacer3", 
                     "dr4", "dr5", "dr6", "spacer4", "spacer5", "spacer6"]
            f.write('\t'.join(fields) + '\n')
            
            r1_opener = gzip.open if r1_file.endswith('.gz') else open
            r2_opener = gzip.open if r2_file.endswith('.gz') else open
            
            with r1_opener(r1_file, 'rt') as r1_f, r2_opener(r2_file, 'rt') as r2_f:
                for idx, (r1_bytes, r2_bytes) in enumerate(zip(r1_f, r2_f)):
                    # Get sequence lines
                    if r1_bytes.startswith('@'):  # Header
                        continue
                    elif r1_bytes.startswith('+'):  # Plus line
                        continue
                    elif r1_bytes.startswith('!'):  # Quality line
                        continue
                    else:  # Sequence line
                        r1_seq = r1_bytes.strip()
                        r2_seq = r2_bytes.strip()
                        
                        # Find DRs and spacers
                        r1_drs = self._find_constants(r1_seq, constant_table, 3)
                        r1_spacers = self._find_spacers_in_tuple_table(r1_seq, tuple_table)[:3]
                        r2_drs = self._find_constants(r2_seq, constant_table, 3)
                        r2_spacers = self._find_spacers_in_tuple_table(r2_seq, tuple_table)[:3]
                        
                        # Reverse R2 results
                        r2_drs.reverse()
                        r2_spacers.reverse()
                        
                        # Write results
                        result = [str(idx)]
                        result.extend(r1_drs + [''] * (3 - len(r1_drs)))
                        result.extend(r1_spacers + [''] * (3 - len(r1_spacers)))
                        result.extend(r2_drs + [''] * (3 - len(r2_drs)))
                        result.extend(r2_spacers + [''] * (3 - len(r2_spacers)))
                        
                        f.write('\t'.join(result) + '\n')
        
        print(f"Read descriptions saved to: {output_file}")
    
    def _find_matching_construct(self, r1_seq: str, r2_seq: str) -> Optional[int]:
        """Find matching construct ID for given R1 and R2 sequences"""
        # Check if R1 sequence matches any construct
        r1_matches = set()
        for seq, cids in self.r1_table.items():
            if seq in r1_seq:
                r1_matches.update(cids)
        
        # Check if R2 sequence matches any construct
        r2_matches = set()
        for seq, cids in self.r2_table.items():
            if seq in r2_seq:
                r2_matches.update(cids)
        
        # Find intersection
        intersection = r1_matches & r2_matches
        
        if len(intersection) == 1:
            return list(intersection)[0]
        elif len(intersection) > 1:
            print(f"Warning: Ambiguous match found for R1={r1_seq[:50]}... R2={r2_seq[:50]}...")
            return None
        else:
            return None
    
    def _find_spacers(self, sequence: str, spacer_table: SpacerTable, max_count: int = None) -> List[str]:
        """Find spacers in sequence"""
        spacers = []
        for kmer in KmerIter(sequence, spacer_table.spacer_length()):
            spacer = spacer_table.contains(kmer)
            if spacer:
                spacers.append(spacer)
                if max_count and len(spacers) >= max_count:
                    break
        return spacers
    
    def _find_constants(self, sequence: str, constant_table: ConstantTable, max_count: int = None) -> List[str]:
        """Find constants in sequence"""
        constants = []
        for kmer in KmerIter(sequence, constant_table.k()):
            constant = constant_table.get_constant(kmer)
            if constant:
                constants.append(constant.sequence)
                if max_count and len(constants) >= max_count:
                    break
        return constants
    
    def _find_matching_tuple(self, r1_seq: str, r2_seq: str, tuple_table: TupleTable) -> Optional[int]:
        """Find matching tuple for given sequences - matches original casmap logic"""
        # Find spacers in R1 and R2
        r1_spacers = self._find_spacers_in_tuple_table(r1_seq, tuple_table)
        r2_spacers = self._find_spacers_in_tuple_table(r2_seq, tuple_table)
        
        # For 4-plex: need 4 spacers total
        if tuple_table.spacer_count == 4:
            if len(r1_spacers) >= 2 and len(r2_spacers) >= 2:
                # Try to find matching 4-tuple
                for i in range(len(r1_spacers) - 1):
                    for j in range(len(r2_spacers) - 1):
                        tuple_4 = (r1_spacers[i], r1_spacers[i+1], r2_spacers[j], r2_spacers[j+1])
                        cid = tuple_table.get_tuple_4(tuple_4)
                        if cid is not None:
                            return cid
        
        # For 6-plex: need 6 spacers total
        elif tuple_table.spacer_count == 6:
            if len(r1_spacers) >= 3 and len(r2_spacers) >= 3:
                # Try to find matching 6-tuple
                for i in range(len(r1_spacers) - 2):
                    for j in range(len(r2_spacers) - 2):
                        tuple_6 = (r1_spacers[i], r1_spacers[i+1], r1_spacers[i+2], 
                                  r2_spacers[j], r2_spacers[j+1], r2_spacers[j+2])
                        cid = tuple_table.get_tuple_6(tuple_6)
                        if cid is not None:
                            return cid
        
        return None
    
    def _find_spacers_in_tuple_table(self, sequence: str, tuple_table: TupleTable) -> List[str]:
        """Find spacers in sequence using tuple table"""
        spacers = []
        for kmer in KmerIter(sequence, tuple_table.k()):
            spacer = tuple_table.get_spacer(kmer)
            if spacer:
                spacers.append(spacer)
        return spacers
    
    def save_results(self, counts: Dict[int, int], output_file: str):
        """Save results to TSV file"""
        with open(output_file, 'w') as f:
            f.write("ConstructID\tCounts\n")
            for cid in sorted(counts.keys()):
                f.write(f"{cid}\t{counts[cid]}\n")
        print(f"Results saved to: {output_file}") 