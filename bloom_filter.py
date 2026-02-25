from typing import Callable, Tuple

import mmh3
import numpy as np
import bitarray

class BloomFilter:
    def __init__(self, k: int, m: int,
                 hash_func: Callable[[str], int] = mmh3.hash64):
        if k <= 0 or m <= 0:
            raise ValueError("K and m must be higher than 0")
        self._m = m
        self._k = k
        self._counters = bitarray.bitarray(self._m)
        self._hash_func = hash_func

    @classmethod
    def make_filter_with_specified_accuracy(cls, eps: float, n: int,
                                            hash_func: Callable[[str], int] = mmh3.hash64):
        k, m = cls._calculate_k_and_m__with_specified_accuracy(eps, n)

        return cls(k, m, hash_func)

    @staticmethod
    def _calculate_k_and_m__with_specified_accuracy(eps: float, n: int,) -> Tuple[int, int]:
        m = int(np.ceil(-n * np.log(eps) / (np.log(2) ** 2)))
        k = int(np.ceil(m * np.log(2) / n))
        return k, m
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


    def _get_hash(self, element: str, number_of_function: int) -> None:
        return self._hash_func(str(number_of_function) + element) % (2**30)


    def element_is_in_filter(self, element: str) -> None:
        for number_of_hash_func in range(self._k):
            number = self._get_hash(element, number_of_hash_func) % self._m
            if self._counters[number] == 0:
                return False
        return True
