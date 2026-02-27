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

    def __add__(self, other):
        if self.m != other.m:
            raise ValueError("Filters must have same m")

        union_filter = BloomFilter(self.k, self.m)
        union_filter._counters = [self._counters[i] + other._counters[i]
                                  for i in range(self.m)]

        return union_filter

    @staticmethod
    def intersect_filters(bf1, bf2):
        if bf1.m != bf2.m:
            raise ValueError("Filters must have same m")

        intersect_filter = BloomFilter(bf1.k, bf1.m)
        intersect_filter._counters = [min(bf1._counters[i], bf2._counters[i])
                                      for i in range(bf1.m)]

        return intersect_filter