# COMP3506 — Data Structures and Algorithms

Two assignments from COMP3506/7505 at UQ implementing core data structures and algorithms from scratch in Python.

## Assignment 1 — Data Structures & Algorithms

### Structures implemented from scratch
- **DynamicArray** — resizable array with O(1) amortised append
- **LinkedList** — doubly linked list
- **BitVector** — compact bit array
- **BloomFilter** — probabilistic membership structure using FNV-1a hashing
- **HashMap** — hash map with open addressing
- **PriorityQueue** — min-heap based priority queue
- **Graph / LatticeGraph** — adjacency list graph representations

### Algorithms
- **BFS** — Breadth-First Search on general and lattice graphs
- **Dijkstra's** — shortest path with priority queue
- **Huffman Coding** — greedy compression algorithm (`compress.py`)
- **Problem solving** (`problems.py`) — various algorithmic challenges using the above structures

## Assignment 2 — K-mer Querying (MallocLabs)

A specialised data structure for DNA sequence analysis:

- **KmerStore** (`kmer_structure.py`) — stores and queries k-mers (fixed-length DNA substrings) with prefix-based lookup
- Builds on extended versions of DynamicArray, LinkedList, and BitVector from A1
- Includes a DNA sequence generator for testing
- Written analysis of time/space complexity in `analysis.txt`

## Structure

```
assignment1/
├── structures/     # DynamicArray, LinkedList, BitVector, BloomFilter, Map, PQueue, Graph
└── algorithms/     # BFS, Dijkstra, Huffman compression, problem solving

assignment2/
├── structures/     # Extended data structures
├── malloclabs/     # KmerStore implementation + DNA generator + analysis
└── warmup/         # Warmup problems (hashing, binary search, merge sort)
```

## Tech Stack

- Python 3
- No external libraries — all structures built from scratch
