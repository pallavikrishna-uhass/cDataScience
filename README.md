# Bloom Filter Implementation in Python
## Team Members

- Mikita Bisliuk (Add student number)
- Pallavi Krishna (2469603)


# This project implements a Bloom Filter in Python 

This project was developed for the Concepts of Data Science (2025–2026) course.

The goal of the project is to implement, test, and evaluate a Bloom Filter data structure in Python. 
A Bloom Filter is a probabilistic data structure that provides highly memory-efficient membership testing.

Bloom Filters can determine:

whether an element is definitely not present
whether an element is probably present

Bloom Filters may produce false positives but never false negatives.

https://datamanagement.hms.harvard.edu/collect-analyze/documentation-metadata/readme-files 

# Repository Structure 

```text
cDataScience/
│
├── src/
│   └── bloom_filter/
│       ├── __init__.py
│       ├── base.py
│       ├── bloom.py
│       └── hashes.py
│
├── tests/
│   ├── test_bloom.py
│   └── test_hashes.py
│
├── benchmarks/
│   ├── benchmark.py
│   ├── false_positive.py
│   ├── compression.py
│   └── job.slurm
│
├── notebooks/
│   └── demo.ipynb
│
├── plots/
│
├── README.md
├── requirements.txt
└── environment.yml
```

---

# Bloom Filter Overview

The Bloom Filter uses:
- a fixed-size bit array
- multiple hash functions

## Insert Operation

When an item is inserted:
1. The item is passed through multiple hash functions
2. Each hash function produces an index
3. Corresponding bits are set to 1

## Search Operation

To check whether an item exists:
1. The same hash functions are applied
2. Corresponding bits are checked

Results:
- If any bit is 0 → item is definitely not present
- If all bits are 1 → item is probably present

---

# Features

# Implementations

Three Bloom Filter implementations were developed and compared.

## BloomFilter

The primary implementation.

### Features

- Object-oriented design
- Automatic calculation of optimal bit-array size
- Automatic calculation of optimal number of hash functions
- SHA256-based hash family
- Bytearray-based storage
- Estimated false-positive rate calculation
- Memory usage tracking

### Focus

- Accuracy
- Reliability
- Theoretical correctness

---

## BloomFilter_01

A simplified educational implementation.

### Features

- Fixed-size bit array implemented as a Python list
- Simplified hash family
- Fixed number of hash functions

### Focus

- Simplicity
- Readability
- Educational comparison baseline

---

## BloomFilter_02

A performance-oriented implementation.

### Features

- Inherits from `BloomFilter`
- Bytearray storage
- Automatic sizing
- Lightweight hash family
- Reduced hashing overhead

### Focus

- Faster execution
- Reduced computational cost

---

# Hash Function Families

The project includes multiple hash-family implementations.

## HashFunctionFamily

Uses SHA256 hashing and double hashing to generate multiple independent hash functions.

### Characteristics

- High-quality distribution
- Deterministic output
- Strong resistance to collisions

---

## HashFunctionFamily_01

Simplified custom hash implementation.

### Characteristics

- Faster computation
- Less uniform distribution
- Higher false-positive rates under heavy load

---

## HashFunctionFamily_03

Performance-oriented implementation based on Python's built-in hashing.

### Characteristics

- Reduced computational overhead
- Faster execution
- Slightly reduced accuracy compared to SHA256

---


# Installation

## Clone Repository

```bash
git clone <repository-url>
cd cDataScience
```

## Create Conda Environment

```bash
conda create -n bloom python=3.11
conda activate bloom
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---
# Dependencies

Main packages used:
- numpy
- matplotlib
- pytest
- mmh3

---

# Usage

```python
from src.bloom_filter import BloomFilter

bf = BloomFilter(
    capacity=10000,
    error_rate=0.01,
)

bf.add("apple")

print(bf.contains("apple"))
print(bf.contains("banana"))
```

Expected output:

```text
True
False
```


---

# Running Tests

The project uses `pytest`.

Run all tests:

```bash
pytest
```

Run Bloom Filter tests only:

```bash
pytest tests/test_bloom.py
```

Run hash-function tests only:

```bash
pytest tests/test_hashes.py
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

---

# Hash Function Testing

The hash functions were evaluated using:

- Natural language words
- Random strings
- DNA sequences
- Numeric strings
- Unicode strings

The tests verify:

- Deterministic behaviour
- Valid index generation
- Distribution quality
- Collision resistance
- Consistency across data types

---

# Performance Benchmarking

Performance benchmarks compare all Bloom Filter implementations.

Metrics measured:

- Insert throughput
- Membership-query throughput
- False-positive rate

Benchmark command:

```bash
python3 benchmarks/benchmark.py --samples 10000
```

---

# Preliminary Benchmark Results

## 1,000 Elements

| Implementation | Operations/sec | False Positive Rate |
|----------------|---------------:|--------------------:|
| BloomFilter | 110,496 | 0.0000 |
| BloomFilter_01 | 275,378 | 0.0070 |
| BloomFilter_02 | 262,402 | 0.0040 |

## 10,000 Elements

| Implementation | Operations/sec | False Positive Rate |
|----------------|---------------:|--------------------:|
| BloomFilter | 112,216 | 0.0106 |
| BloomFilter_01 | 288,601 | 0.9900 |
| BloomFilter_02 | 267,709 | 0.0324 |

## 100,000 Elements

| Implementation | Operations/sec | False Positive Rate |
|----------------|---------------:|--------------------:|
| BloomFilter | 113,345 | 0.9946 |
| BloomFilter_01 | 287,878 | 1.0000 |
| BloomFilter_02 | 268,631 | 0.9956 |


Plots are available in the `plots/` directory.

### Discussion


The results demonstrate the trade-off between speed and accuracy.

- **BloomFilter** provides the lowest false-positive rates when operating within its design capacity but is slower due to SHA256 hashing.
- **BloomFilter_01** achieves the highest throughput but rapidly loses accuracy once the filter becomes saturated.
- **BloomFilter_02** offers a compromise between performance and accuracy by using a lighter-weight hashing strategy.

All implementations exhibit substantially increased false-positive rates when the number of inserted elements greatly exceeds the filter's configured capacity (10,000 elements), illustrating a fundamental limitation of Bloom Filters.


---

# HPC Benchmarking

Benchmarking experiments were performed on HPC infrastructure.

Included files:
- `benchmark.py`
- `run_benchmark.sh`
- benchmark output log

## Running on HPC

```bash
sbatch run_benchmark.sh
```

---

# False Positive Analysis

The project evaluates how the false positive rate changes:
- as more items are inserted
- when the Bloom Filter exceeds its designed capacity

Results demonstrate that:
- false positive rate increases as the filter fills
- overloading the filter significantly reduces accuracy

---

# Compression Analysis

The Bloom Filter memory usage was compared against:
- Python sets
- direct storage of strings

The analysis demonstrates:
- significant memory savings
- trade-offs between accuracy and storage efficiency

---

# Time Complexity

## Insert Operation

O(k)

## Search Operation

O(k)

Where:
- k = number of hash functions

---

# Space Complexity

O(m)

Where:
- m = size of the bit array

---

# Results Summary

# Conclusions

The project demonstrates that Bloom Filters provide:

- Efficient memory usage
- Fast membership testing
- Configurable accuracy-performance trade-offs

The experiments show that implementation choices, hash-function design, and filter capacity significantly influence performance and false-positive behaviour.

The benchmarking results also highlight that Bloom Filters must be configured appropriately for the expected dataset size; otherwise, false-positive rates increase dramatically as the filter becomes saturated.


---

# Future Improvements

Possible improvements include:
- Counting Bloom Filters
- Dynamic Bloom Filters
- Parallel hash computation
- Optimised bit arrays using NumPy

---

Programs and Code used for Concepts of Data Science - Masters in Statistics and Data Science
