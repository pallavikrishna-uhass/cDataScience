"""
Tests for the BloomFilter class.

"""

import random
import string

import pytest

from src.bloom_filter.bloom import BloomFilter


class TestBloomFilterInitialization:
    """Tests for BloomFilter initialization."""

    def test_initialization_valid_parameters(self) -> None:
        """Test that valid parameters are accepted."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert bf.capacity == 1000
        assert bf.error_rate == 0.01
        assert bf.count == 0

    def test_initialization_custom_seed(self) -> None:
        """Test that custom seed is stored."""
        bf = BloomFilter(capacity=100, error_rate=0.01, seed=123)
        assert bf.seed == 123

    def test_initialization_invalid_capacity_zero(self) -> None:
        """Test that zero capacity raises error."""
        with pytest.raises(ValueError, match="capacity must be a positive integer"):
            BloomFilter(capacity=0, error_rate=0.01)

    def test_initialization_invalid_capacity_negative(self) -> None:
        """Test that negative capacity raises error."""
        with pytest.raises(ValueError, match="capacity must be a positive integer"):
            BloomFilter(capacity=-100, error_rate=0.01)

    def test_initialization_invalid_error_rate_zero(self) -> None:
        """Test that zero error rate raises error."""
        with pytest.raises(ValueError, match="error_rate must be in range"):
            BloomFilter(capacity=100, error_rate=0)

    def test_initialization_invalid_error_rate_one(self) -> None:
        """Test that error rate of 1 raises error."""
        with pytest.raises(ValueError, match="error_rate must be in range"):
            BloomFilter(capacity=100, error_rate=1)

    def test_initialization_invalid_error_rate_negative(self) -> None:
        """Test that negative error rate raises error."""
        with pytest.raises(ValueError, match="error_rate must be in range"):
            BloomFilter(capacity=100, error_rate=-0.5)

    def test_optimal_bit_array_size_calculation(self) -> None:
        """Test that bit array size is calculated correctly."""
        # For capacity=1000, error_rate=0.01
        # m = -1000 * ln(0.01) / (ln(2)^2) ≈ 9586
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert bf.bit_array_size == 9586

    def test_optimal_hash_functions_calculation(self) -> None:
        """Test that number of hash functions is calculated correctly."""
        # For m=9586, n=1000
        # k = (9586/1000) * ln(2) ≈ 6.65 ≈ 7
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert bf.num_hash_functions == 7

    def test_lower_error_rate_requires_more_memory(self) -> None:
        """Test that lower error rates require larger bit arrays."""
        bf_low = BloomFilter(capacity=1000, error_rate=0.001)
        bf_high = BloomFilter(capacity=1000, error_rate=0.1)
        assert bf_low.bit_array_size > bf_high.bit_array_size

    def test_higher_capacity_requires_more_memory(self) -> None:
        """Test that higher capacity requires larger bit arrays."""
        bf_small = BloomFilter(capacity=100, error_rate=0.01)
        bf_large = BloomFilter(capacity=10000, error_rate=0.01)
        assert bf_large.bit_array_size > bf_small.bit_array_size


class TestBloomFilterBasicOperations:
    """Tests for basic Bloom filter operations."""

    def test_add_single_element(self) -> None:
        """Test adding a single element."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("test")
        assert bf.count == 1

    def test_add_multiple_elements(self) -> None:
        """Test adding multiple elements."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("apple")
        bf.add("banana")
        bf.add("cherry")
        assert bf.count == 3

    def test_add_duplicate_element(self) -> None:
        """Test that adding duplicate doesn't increase count."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("test")
        bf.add("test")
        bf.add("test")
        assert bf.count == 1

    def test_contains_added_element(self) -> None:
        """Test that added elements are found."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("test")
        assert bf.contains("test") is True

    def test_contains_not_added_element(self) -> None:
        """Test that non-added elements are (usually) not found."""
        bf = BloomFilter(capacity=1000, error_rate=0.001)
        bf.add("apple")
        # With low error rate, "orange" should not be found
        assert bf.contains("orange") is False

    def test_in_operator(self) -> None:
        """Test Python's 'in' operator."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("test")
        assert "test" in bf
        assert "other" not in bf

    def test_len_operator(self) -> None:
        """Test Python's len() function."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        assert len(bf) == 0
        bf.add("one")
        assert len(bf) == 1
        bf.add("two")
        assert len(bf) == 2

    def test_repr_string(self) -> None:
        """Test string representation."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        repr_str = repr(bf)
        assert "BloomFilter" in repr_str
        assert "capacity=1000" in repr_str
        assert "error_rate=0.01" in repr_str


class TestBloomFilterFalsePositives:
    """Tests for false positive behavior."""

    def test_no_false_negatives(self) -> None:
        """Test that there are no false negatives."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        elements = [f"element_{i}" for i in range(100)]

        for elem in elements:
            bf.add(elem)

        # All added elements must be found (no false negatives)
        for elem in elements:
            assert bf.contains(elem) is True, f"False negative for element: {elem}"

    def test_false_positive_rate_approximately_correct(self) -> None:
        """Test that actual false positive rate is close to target."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)

        # Add 1000 elements
        for i in range(1000):
            bf.add(f"element_{i}")

        # Test 10000 non-elements
        false_positives = 0
        for i in range(10000):
            if bf.contains(f"nonexistent_{i}"):
                false_positives += 1

        actual_rate = false_positives / 10000
        # Allow some variance, but should be in the ballpark
        assert (
            actual_rate < 0.05
        ), f"False positive rate {actual_rate} too high (target: 0.01)"

    def test_fill_ratio_increases_with_elements(self) -> None:
        """Test that fill ratio increases as elements are added."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)

        initial_ratio = bf.fill_ratio
        assert initial_ratio == 0.0

        bf.add("element_1")
        ratio_after_one = bf.fill_ratio
        assert ratio_after_one > 0

        for i in range(100):
            bf.add(f"element_{i}")

        ratio_after_many = bf.fill_ratio
        assert ratio_after_many > ratio_after_one

    def test_estimated_error_rate_increases_with_fill(self) -> None:
        """Test that estimated error rate increases as filter fills."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)

        initial_rate = bf.estimated_error_rate()
        assert initial_rate == 0.0

        for i in range(500):
            bf.add(f"element_{i}")

        later_rate = bf.estimated_error_rate()
        assert later_rate > initial_rate


class TestBloomFilterSpecialOperations:
    """Tests for special operations."""

    def test_clear_removes_all_elements(self) -> None:
        """Test that clear removes all elements."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("apple")
        bf.add("banana")
        bf.clear()

        assert bf.count == 0
        assert "apple" not in bf
        assert "banana" not in bf

    def test_clear_resets_fill_ratio(self) -> None:
        """Test that clear resets fill ratio to zero."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        for i in range(50):
            bf.add(f"element_{i}")

        assert bf.fill_ratio > 0
        bf.clear()
        assert bf.fill_ratio == 0.0

    def test_memory_size_bytes(self) -> None:
        """Test memory size calculation."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        # bit_array_size is 9586, so bytes should be 9586 // 8 + 1 = 1199
        assert bf.memory_size_bytes == 1199


class TestBloomFilterWithDataTypes:
    """Tests with different data types."""

    def test_natural_language_words(self) -> None:
        """Test with natural language words."""
        bf = BloomFilter(capacity=100, error_rate=0.01)

        words = [
            "the",
            "be",
            "to",
            "of",
            "and",
            "a",
            "in",
            "that",
            "have",
            "it",
            "for",
            "not",
            "on",
            "with",
            "he",
            "as",
            "you",
            "do",
            "at",
            "this",
        ]

        for word in words:
            bf.add(word)

        # All words should be found
        for word in words:
            assert word in bf, f"Word not found: {word}"

    def test_random_strings(self) -> None:
        """Test with random alphanumeric strings."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        random.seed(42)

        strings = [
            "".join(random.choices(string.ascii_letters + string.digits, k=20))
            for _ in range(100)
        ]

        for s in strings:
            bf.add(s)

        # All strings should be found
        for s in strings:
            assert s in bf, f"String not found: {s}"

    def test_dna_sequences(self) -> None:
        """Test with DNA sequences."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        random.seed(42)
        bases = ["A", "C", "G", "T"]

        sequences = ["".join(random.choices(bases, k=100)) for _ in range(100)]

        for seq in sequences:
            bf.add(seq)

        # All sequences should be found
        for seq in sequences:
            assert seq in bf, f"Sequence not found: {seq}"

    def test_numeric_strings(self) -> None:
        """Test with numeric strings."""
        bf = BloomFilter(capacity=1000, error_rate=0.01)

        for i in range(1000):
            bf.add(str(i))

        # All numbers should be found
        for i in range(1000):
            assert str(i) in bf, f"Number not found: {i}"


class TestBloomFilterEdgeCases:
    """Tests for edge cases."""

    def test_empty_string(self) -> None:
        """Test with empty string."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("")
        assert "" in bf

    def test_very_long_string(self) -> None:
        """Test with very long string."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        long_string = "a" * 1000000  # 1 million characters
        bf.add(long_string)
        assert long_string in bf

    def test_unicode_characters(self) -> None:
        """Test with Unicode characters."""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        unicode_strings = ["你好", "こんにちは", "Привет", "مرحبا", "🎉🎊"]

        for s in unicode_strings:
            bf.add(s)

        for s in unicode_strings:
            assert s in bf, f"Unicode string not found: {s}"

    def test_single_element_filter(self) -> None:
        """Test filter with capacity for single element."""
        bf = BloomFilter(capacity=1, error_rate=0.01)
        bf.add("only")
        assert "only" in bf

    def test_minimum_hash_functions(self) -> None:
        """Test that at least one hash function is used."""
        # Even with extreme parameters, should have at least 1 hash function
        bf = BloomFilter(capacity=1, error_rate=0.5)
        assert bf.num_hash_functions >= 1
