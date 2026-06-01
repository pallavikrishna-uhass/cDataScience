"""
Tests for the hash function family.

"""

import pytest

from src.bloom_filter.hashes import HashFunctionFamily


class TestHashFunctionFamily:
    """Tests for the HashFunctionFamily class."""

    def test_initialization_valid_parameters(self) -> None:
        """Test that valid parameters are accepted."""
        hasher = HashFunctionFamily(num_functions=7, size=1000)
        assert hasher.num_functions == 7
        assert hasher.size == 1000
        assert hasher.seed == 42  # Default seed

    def test_initialization_with_custom_seed(self) -> None:
        """Test that custom seed is stored."""
        hasher = HashFunctionFamily(num_functions=5, size=500, seed=123)
        assert hasher.seed == 123

    def test_initialization_invalid_num_functions(self) -> None:
        """Test that zero or negative num_functions raises error."""
        with pytest.raises(ValueError, match="num_functions must be at least 1"):
            HashFunctionFamily(num_functions=0, size=1000)
        with pytest.raises(ValueError, match="num_functions must be at least 1"):
            HashFunctionFamily(num_functions=-1, size=1000)

    def test_initialization_invalid_size(self) -> None:
        """Test that zero or negative size raises error."""
        with pytest.raises(ValueError, match="size must be at least 1"):
            HashFunctionFamily(num_functions=7, size=0)
        with pytest.raises(ValueError, match="size must be at least 1"):
            HashFunctionFamily(num_functions=7, size=-100)

    def test_hash_returns_correct_number_of_indices(self) -> None:
        """Test that hash returns exactly k indices."""
        hasher = HashFunctionFamily(num_functions=7, size=1000)
        indices = hasher.hash("test")
        assert len(indices) == 7

    def test_hash_indices_within_valid_range(self) -> None:
        """Test that all hash indices are in range [0, size)."""
        hasher = HashFunctionFamily(num_functions=10, size=1000)
        for data in ["test", "hello", "world", "abc123"]:
            indices = hasher.hash(data)
            assert all(0 <= idx < 1000 for idx in indices)

    def test_hash_deterministic_same_input(self) -> None:
        """Test that same input produces same output (deterministic)."""
        hasher = HashFunctionFamily(num_functions=7, size=1000, seed=42)
        indices1 = hasher.hash("test")
        indices2 = hasher.hash("test")
        assert indices1 == indices2

    def test_hash_different_for_different_inputs(self) -> None:
        """Test that different inputs produce different hash values."""
        hasher = HashFunctionFamily(num_functions=7, size=1000)
        indices1 = hasher.hash("apple")
        indices2 = hasher.hash("banana")
        assert indices1 != indices2

    def test_hash_single_function(self) -> None:
        """Test hash_single method returns single index."""
        hasher = HashFunctionFamily(num_functions=5, size=100)
        for i in range(5):
            idx = hasher.hash_single("test", i)
            assert isinstance(idx, int)
            assert 0 <= idx < 100

    def test_hash_single_invalid_index(self) -> None:
        """Test hash_single with invalid function_index."""
        hasher = HashFunctionFamily(num_functions=5, size=100)
        with pytest.raises(ValueError, match="function_index must be in range"):
            hasher.hash_single("test", 5)  # Out of range
        with pytest.raises(ValueError, match="function_index must be in range"):
            hasher.hash_single("test", -1)


class TestHashFunctionIndependence:
    """Test that hash functions in the family are independent."""

    def test_different_functions_produce_different_indices(self) -> None:
        """Test that different hash functions produce different indices."""
        hasher = HashFunctionFamily(num_functions=7, size=1000)

        # Get indices from each individual hash function
        all_indices = []
        for i in range(hasher.num_functions):
            idx = hasher.hash_single("test_data", i)
            all_indices.append(idx)

        # Most functions should produce different indices
        unique_indices = len(set(all_indices))
        assert (
            unique_indices >= hasher.num_functions - 1
        ), "Too many hash functions producing identical indices"

    def test_cross_data_type_consistency(self) -> None:
        """Test hash behavior is consistent across different data types."""
        hasher = HashFunctionFamily(num_functions=7, size=1000)

        test_cases = [
            ("natural", "hello world"),
            ("random", "aB3dE5gH7j"),
            ("dna", "ATCGATCGATCG"),
            ("numeric", "123456789"),
            ("mixed", "Test_123_DNA"),
        ]

        for name, data in test_cases:
            indices = hasher.hash(data)
            assert len(indices) == 7, f"Failed for {name}"
            assert all(0 <= idx < 1000 for idx in indices), f"Failed for {name}"
