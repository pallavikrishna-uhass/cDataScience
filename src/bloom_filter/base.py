from typing import Any


class BaseFilter:
    """
    Base class for Bloom filter implementations.
    """

    def add(self, item: Any) -> None:
        """Add an item to the filter"""
        raise NotImplementedError

    def contains(self, item: Any) -> bool:
        """Check if item might be in the filter"""
        raise NotImplementedError
