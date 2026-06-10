import hashlib


class HashFunctionFamily:
    """
    A family of hash functions for Bloom filter usage.

    This class generates multiple independent hash functions from two base
    hash functions using the double hashing technique. Each hash function
    in the family maps input data to an index in the range [0, size).

    """

    def __init__(self, num_functions: int, size: int, seed: int = 42) -> None:
        if num_functions < 1:
            raise ValueError("num_functions must be at least 1")
        if size < 1:
            raise ValueError("size must be at least 1")

        self.num_functions = num_functions
        self.size = size
        self.seed = seed

    def _base_hash(self, data: bytes, salt: int) -> int:
        # Combine salt with data to create independent hash functions
        salted_data = f"{salt}:{self.seed}:".encode() + data
        hash_digest = hashlib.sha256(salted_data).hexdigest()
        # Convert first 16 hex characters (64 bits) to integer
        return int(hash_digest[:16], 16)

    def hash(self, data: str) -> list[int]:
        data_bytes = data.encode("utf-8")

        # Compute two base hash values
        h1 = self._base_hash(data_bytes, salt=1)
        h2 = self._base_hash(data_bytes, salt=2)

        # Generate k hash functions using double hashing: h_i = h1 + i * h2
        indices: list[int] = []
        for i in range(self.num_functions):
            combined_hash = (h1 + i * h2) % (2**64)  # Keep within 64-bit range
            indices.append(combined_hash % self.size)

        return indices

    def hash_single(self, data: str, function_index: int) -> int:
        if not 0 <= function_index < self.num_functions:
            raise ValueError(
                f"function_index must be in range [0, {self.num_functions})"
            )

        data_bytes = data.encode("utf-8")
        h1 = self._base_hash(data_bytes, salt=1)
        h2 = self._base_hash(data_bytes, salt=2)

        combined_hash = (h1 + function_index * h2) % (2**64)
        return combined_hash % self.size

class HashFunctionFamily_01:
    """
    Simplified custom hash family.

    Generates multiple hash values using basic arithmetic
    and string processing operations.

    Characteristics:
    - easy to understand
    - fast computation
    - suitable for educational purposes

    Trade-off:
    - weaker distribution quality
    - higher collision probability
    """

    def __init__(self, num_functions, size):
        self.num_functions = num_functions
        self.size = size

        if num_functions < 1:
            raise ValueError("num_functions must be at least 1")
        if size < 1:
            raise ValueError("size must be at least 1")

    def hash(self, data):
        indices = []

        for i in range(self.num_functions):
            h = hash(f"{i}-{data}")
            indices.append(h % self.size)

        return indices
    
class HashFunctionFamily_02:
    """
    Lightweight performance-oriented hash family.

    Uses Python's built-in hashing combined with simple
    rehashing techniques to generate multiple indices.

    Characteristics:
    - fast execution
    - low computational overhead
    - suitable for benchmarking

    Trade-off:
    - lower distribution quality than SHA256
    - increased false-positive rates at high load factors
    """

    def __init__(
        self,
        num_functions: int,
        size: int,
        seed: int = 42,
    ) -> None:

        if num_functions < 1:
            raise ValueError(
                "num_functions must be at least 1"
            )

        if size < 1:
            raise ValueError(
                "size must be at least 1"
            )

        self.num_functions = num_functions
        self.size = size
        self.seed = seed

    def hash(self, data: str) -> list[int]:

        h1 = hash((data, self.seed))
        h2 = hash((data, self.seed + 1))

        return [
            (h1 + i * h2) % self.size
            for i in range(self.num_functions)
        ]

    def hash_single(
        self,
        data: str,
        function_index: int,
    ) -> int:

        if not 0 <= function_index < self.num_functions:
            raise ValueError(
                f"function_index must be in range "
                f"[0, {self.num_functions})"
            )

        h1 = hash((data, self.seed))
        h2 = hash((data, self.seed + 1))

        return (
            h1 + function_index * h2
        ) % self.size