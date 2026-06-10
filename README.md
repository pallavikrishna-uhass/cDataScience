# Bloom Filter Implementation in Python
## Team Members

- Mikita Bisliuk (Add student number)
- Pallavi Krishna (2469603)


# This project implements a Bloom Filter in Python 

A Bloom Filter is a space efficient storage system that helps determine whether an object is present in the dataset

https://datamanagement.hms.harvard.edu/collect-analyze/documentation-metadata/readme-files 

# Repository Structure 
Sample only to fill as the project proceeds

bloom-filter-project/
│
├── bloomfilter/    #Explanation to add
│   ├── __init__.py #Explanation to add
│   ├── bloom.py    #Explanation to add
│   └── hashes.py   #Explanation to add
│
├── tests/          #Explanation to add
│   ├── test_bloom.py   #Explanation to add
│   └── test_hashes.py  #Explanation to add
│
├── benchmark/
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
├── data/
│
├── README.md
├── requirements.txt
└── environment.yml

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

- Object-oriented Bloom Filter implementation
- Multiple hash functions using MurmurHash
- Unit testing with pytest
- False positive rate analysis
- Compression ratio analysis
- Performance benchmarking
- HPC-compatible benchmark scripts
- Plot generation using matplotlib

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd bloom-filter-project
```

---

## Create Conda Environment

```bash
conda create -n bloom python=3.11
conda activate bloom
```

---

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

## Example

```python
from bloomfilter.bloom import BloomFilter

bf = BloomFilter(size=10000, num_hashes=3)

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

The project uses pytest for testing.

Run all tests:

```bash
pytest
```

---

# Hash Function Testing

The hash functions were tested using:
1. Natural language words
2. Randomly generated strings

The tests evaluate:
- consistency
- distribution quality
- collision behaviour

---

# Performance Benchmarking

Benchmarks were performed for increasing dataset sizes:
- 1,000 words
- 10,000 words
- 100,000 words
- 1,000,000 words

The following metrics were measured:
- insertion time
- lookup time

Plots are available in the `plots/` directory.

---

# HPC Benchmarking

Benchmarking experiments were performed on HPC infrastructure.

Included files:
- `benchmark.py`
- `job.slurm`
- benchmark output logs

## Running on HPC

```bash
sbatch job.slurm
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

Key findings:
- Bloom Filters provide extremely fast membership checks
- Memory usage is significantly lower than storing raw data
- False positive rates increase with filter saturation
- Proper selection of filter size and hash count is critical

---

# Future Improvements

Possible improvements include:
- Counting Bloom Filters
- Dynamic Bloom Filters
- Parallel hash computation
- Optimised bit arrays using NumPy

---

Programs and Code used for Concepts of Data Science - Masters in Statistics and Data Science
