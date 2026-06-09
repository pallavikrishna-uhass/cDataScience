"""
Bloom Filter Benchmarking Script

Compares all Bloom filter implementations for performance and accuracy.

Usage:
    python benchamrks/benchmark.py [--samples N]
"""

import argparse
import random
import string
import sys
import time
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, ".")

from src.bloom_filter import BaseFilter, BloomFilter, BloomFilter_01


@dataclass
class BenchmarkResult:
    """Container for benchmark results."""

    implementation: str
    samples: int
    elapsed_time: float
    operations_per_second: float
    false_positive_rate: float
    success: bool
    error_message: Optional[str] = None


def generate_data(n: int) -> list[str]:
    """Generate test data"""
    symbols = string.ascii_letters + string.digits
    return ["".join(random.choices(symbols, k=20)) for _ in range(n)]


def run_benchmark(bf: BaseFilter, samples: int) -> BenchmarkResult:
    """Run benchmark for a single filter implementation"""

    try:
        elements = generate_data(samples)
        non_members = generate_data(samples)

        # Benchmark add operations
        start = time.perf_counter()
        for elem in elements:
            bf.add(elem)
        add_time = time.perf_counter() - start

        # Benchmark contains operations
        start = time.perf_counter()
        found = sum(1 for elem in elements if elem in bf)
        contains_time = time.perf_counter() - start

        # Measure false positive rate
        false_positives = sum(1 for elem in non_members if elem in bf)
        fp_rate = false_positives / len(non_members)

        total_time = add_time + contains_time
        ops_per_second = 2 * samples / total_time

        return BenchmarkResult(
            implementation=bf.__class__.__name__,
            samples=samples,
            elapsed_time=total_time,
            operations_per_second=round(ops_per_second),
            false_positive_rate=round(fp_rate, 6),
            success=True,
        )

    except Exception as e:
        return BenchmarkResult(
            implementation=bf.__class__.__name__,
            samples=samples,
            elapsed_time=0,
            operations_per_second=0,
            false_positive_rate=0,
            success=False,
            error_message=str(e),
        )


def main() -> int:

    parser = argparse.ArgumentParser(description="Bloom Filter Benchmarking Script")
    parser.add_argument("--samples", type=int, default=10000, help="Number of samples")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--output", type=str, default=None, help="Output json file")

    args = parser.parse_args()

    # Filter instances - sonfigure arguments here!
    filters = [
        BloomFilter(capacity=10000, error_rate=0.01),
        BloomFilter_01(size=10000, num_hashes=7),
    ]

    print("=" * 70)
    print("Bloom Filter Benchmark - Implementation Comparison")
    print("=" * 70)
    print(f"Samples: {args.samples:,}")
    print()

    all_results = []

    print(f"{'Implementation':<20} {'Ops/sec':>12} {'FP rate':>10} {'Status':>8}")
    for bf in filters:
        result = run_benchmark(bf=bf, samples=args.samples)
        all_results.append(result)

        if result.success:
            print(
                f"{result.implementation:<20} {result.operations_per_second:>12,} "
                f"{result.false_positive_rate:>10.4f}"
            )
        else:
            print(
                f"{result.implementation:<20} {'ERROR':>12} "
                f"  Error: {result.error_message}"
            )

    if args.output:
        with open(args.ouput, "w") as f:
            import json

            json.dump({"results": all_results}, f, indent=4)
        print(f"\nResults written to: {args.output}")

    return 0 if all(r.success for r in all_results) else 1


if __name__ == "__main__":
    sys.exit(main())
