from sqlalchemy.util import counter
from bloom_filter import BloomFilter
from typing import Callable
import mmh3

class BloomCounterFilter(BloomFilter):
    def __init__(self,
                 k: int = None, m: int = None,
                 hash_func: Callable[[str], int] = mmh3.hash128) -> None:
        super().__init__(k, m, hash_func)
        self._counters = [0] * self.m

    def add_element(self, element: str) -> None:
        for number_of_hash_func in range(self._k):
            array_index = self._get_hash(element, number_of_hash_func) % self._m
            self._counters[array_index] += 1

    def remove_element(self, element: str) -> None:
        if not self.element_is_in_filter(element):
            raise ValueError("Element not in the filter")
        for number_of_hush_function in range(self._k):
            count_number = self._get_hash(element, number_of_hush_function) % self._m
            self._counters[count_number] -= 1
