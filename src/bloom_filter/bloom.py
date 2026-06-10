"""
Bloom Filter Implementation.
"""

import math
from typing import Any

from .base import BaseFilter
from .hashes import HashFunctionFamily, HashFunctionFamily_01, HashFunctionFamily_02


class BloomFilter(BaseFilter):
    """
    Primary Bloom filter implementation.

    Uses:
    - automatic bit-array sizing
    - automatic hash-count calculation
    - SHA256-based double hashing
    - bytearray storage
    - exact element tracking
    - false-positive rate estimation

    Focus:
    - accuracy
    - theoretical correctness
    - memory efficiency

    Trade-off:
    - slower hashing due to cryptographic hash functions
    """

    def __init__(self, capacity: int, error_rate: float = 0.01, seed: int = 42) -> None:

        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate must be in range (0, 1)")

        self.capacity = capacity
        self.error_rate = error_rate
        self.seed = seed
        self.count = 0

        # Calculate optimal bit array size: m = -n * ln(p) / (ln(2)^2)
        # where n = capacity, p = error_rate
        self.bit_array_size = self._optimal_bit_array_size(capacity, error_rate)

        # Calculate optimal number of hash functions: k = (m/n) * ln(2)
        self.num_hash_functions = self._optimal_hash_functions(
            self.bit_array_size, capacity
        )

        # Initialize the bit array (all zeros)
        self._bit_array: bytearray = bytearray(self.bit_array_size // 8 + 1)

        # Initialize hash function family
        self._hasher = HashFunctionFamily(
            num_functions=self.num_hash_functions, size=self.bit_array_size, seed=seed
        )

        # Track added elements for exact count (optional, for accuracy tracking)
        self._added_elements: set[str] = set()

    @staticmethod
    def _optimal_bit_array_size(n: int, p: float) -> int:
        return math.ceil(-n * math.log(p) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hash_functions(m: int, n: int) -> int:
        return max(1, round((m / n) * math.log(2)))

    def add(self, item: str) -> None:
        if item in self._added_elements:
            return  # Already added, no need to set bits again

        # Get all hash indices for this item
        indices = self._hasher.hash(item)

        # Set the corresponding bits to 1
        for idx in indices:
            byte_index = idx // 8
            bit_index = idx % 8
            self._bit_array[byte_index] |= 1 << bit_index

        # Track the added element
        self._added_elements.add(item)
        self.count += 1

    def contains(self, item: str) -> bool:
        indices = self._hasher.hash(item)

        # Check if all corresponding bits are set
        for idx in indices:
            byte_index = idx // 8
            bit_index = idx % 8
            if not (self._bit_array[byte_index] & (1 << bit_index)):
                return False

        return True

    def __len__(self) -> int:
        return self.count

    def __repr__(self) -> str:
        return (
            f"BloomFilter(capacity={self.capacity}, "
            f"error_rate={self.error_rate}, count={self.count})"
        )

    @property
    def memory_size_bytes(self) -> int:
        return len(self._bit_array)

    @property
    def fill_ratio(self) -> float:
        set_bits = sum(bin(byte).count("1") for byte in self._bit_array)
        return set_bits / self.bit_array_size

    def estimated_error_rate(self) -> float:
        if self.bit_array_size == 0 or self.num_hash_functions == 0:
            return 0.0

        # p = (1 - e^(-kn/m))^k
        exponent = -self.num_hash_functions * self.count / self.bit_array_size
        return (1 - math.exp(exponent)) ** self.num_hash_functions

    def clear(self) -> None:
        self._bit_array = bytearray(self.bit_array_size // 8 + 1)
        self._added_elements.clear()
        self.count = 0


class BloomFilter_01(BaseFilter):
    """
    Simplified Bloom filter implementation.

    Uses:
    - fixed-size bit array
    - Python list storage
    - fixed number of hash functions
    - lightweight custom hash family

    Focus:
    - simplicity
    - readability
    - educational comparison

    Does NOT:
    - optimise memory usage
    - automatically size the filter
    - estimate false-positive rates
    - track inserted elements

    Trade-off:
    - faster execution but reduced accuracy under heavy load
    """

    def __init__(self, size=10000, num_hashes=5):
        self.size = size
        self.num_hashes = num_hashes

        self.bits = [0] * size

        self.hasher = HashFunctionFamily_01(num_hashes, size)

    def add(self, item):

        for idx in self.hasher.hash(item):
            self.bits[idx] = 1

    def contains(self, item):

        for idx in self.hasher.hash(item):
            if self.bits[idx] == 0:
                return False

        return True


from .hashes import HashFunctionFamily_02


class BloomFilter_02(BloomFilter):
    """
    Performance-oriented Bloom filter variant.

    Uses:
    - automatic sizing
    - bytearray storage
    - optimal hash-count calculation
    - lightweight hash family

    Focus:
    - faster execution
    - reduced hashing overhead
    - lower memory usage

    Does NOT:
    - track inserted elements

    Trade-off:
    - improved speed with slightly reduced hash quality
    """

    def __init__(
        self,
        capacity: int,
        error_rate: float = 0.01,
        seed: int = 42,
    ) -> None:

        super().__init__(capacity, error_rate, seed)

        # Replace SHA256 hasher with lightweight hasher
        self._hasher = HashFunctionFamily_02(
            num_functions=self.num_hash_functions,
            size=self.bit_array_size,
            seed=seed,
        )

        # No exact membership tracking
        self._added_elements = None

    def add(self, item: str) -> None:

        for idx in self._hasher.hash(item):
            byte_index = idx // 8
            bit_index = idx % 8

            self._bit_array[byte_index] |= 1 << bit_index

        self.count += 1

    def clear(self) -> None:

        self._bit_array = bytearray(self.bit_array_size // 8 + 1)

        self.count = 0

    def __repr__(self) -> str:

        return (
            f"BloomFilter_02("
            f"capacity={self.capacity}, "
            f"error_rate={self.error_rate}, "
            f"count={self.count})"
        )
