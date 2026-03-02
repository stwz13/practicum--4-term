from __future__ import annotations

from typing import Callable, Tuple
import mmh3
import numpy as np
import bitarray


class BloomFilter:
    def __init__(self, k: int, m: int,
                 hash_func: Callable[[str], int] = mmh3.hash128):
        if k <= 0 or m <= 0:
            raise ValueError("K and m must be higher than 0")

        self._m = m
        self._k = k

        self._counters = bitarray.bitarray(self._m)
        self._hash_func = hash_func

    @classmethod
    def make_filter_with_specified_accuracy(cls, eps: float, n: int,
                                            hash_func: Callable[[str], int] = mmh3.hash128):
        if n <= 0:
            raise ValueError("n must be higher than 0")
        if not 0 <= eps <= 1:
            raise ValueError("Eps must be higher than 0 and less than 1")
        k, m = cls.calculate_k_and_m__with_specified_accuracy(eps, n)

        return cls(k, m, hash_func)

    @staticmethod
    def calculate_k_and_m__with_specified_accuracy(eps: float, n: int, ) -> Tuple[int, int]:
        m = int(np.ceil(-n * np.log(eps) / (np.log(2) ** 2)))
        k = int(np.ceil(m * np.log(2) / n))
        return k, m

    def remove_element(self, element: str) -> None:
        if not self.element_is_in_filter(element):
            raise ValueError("Element not in the filter")

        for number_of_hush_function in range(self._k):
            count_number = self._get_hash(element, number_of_hush_function) % self._m
            self._counters[count_number] = 0



    @property
    def m(self) -> int:
        return self._m

    @property
    def k(self) -> int:
        return self._k


    def add_element(self, element: str) -> None:
        for number_of_hash_func in range(self._k):
            array_index = self._get_hash(element, number_of_hash_func) % self._m
            self._counters[array_index] = 1


    def _get_hash(self, element: str, number_of_function: int) -> int:
        return self._hash_func(str(number_of_function) + element) % 2**30


    def element_is_in_filter(self, element: str) -> bool:
        for number_of_hash_func in range(self._k):
            number = self._get_hash(element, number_of_hash_func) % self._m
            if self._counters[number] == 0:
                return False
        return True

    def __add__(self, other):
        if self.m != other.m:
            raise ValueError("Filters must have same m")

        union_filter = BloomFilter(self.k, self.m)
        union_filter._counters = [self._counters[i] or other._counters[i]
                                  for i in range(self.m)]

        return union_filter

    @staticmethod
    def intersect_filters(bf1, bf2):
        if bf1.m != bf2.m:
            raise ValueError("Filters must have same m")

        intersect_filter = BloomFilter(bf1.k, bf1.m)
        intersect_filter._counters = [bf1._counters[i] and bf2._counters[i]
                                  for i in range(bf1.m)]

        return intersect_filter



