import mmh3
import numpy as np
import bitarray



class BloomFilter:
    def __init__(self, k: int = None, m: int = None, eps: float = None , n: int = None):
        if eps is not None and n is not None:
            self._m = int(np.ceil(-n * np.log(eps) / (np.log(2) ** 2)))
            self._k = int(np.ceil(self._m * np.log(2) / n))
        elif k is not None and m is not None:
            self._m = m
            self._k = k
        else:
            raise TypeError("Need a pare of parameters k and m or eps and n")
        self._counters = bitarray.bitarray(self._m)


    def add_element(self, element: str):
        for number_of_hash_func in range(self._k):
            array_index = self._get_hash(element, number_of_hash_func) % self._m
            self._counters[array_index] += 1


    @staticmethod
    def _get_hash(element: str, number_of_function: int):
        return mmh3.hash128(str(number_of_function) + element) % (2**30)


    def check_element_in_filter(self, element: str):
        for number_of_hash_func in range(self._k):
            number = self._get_hash(element, number_of_hash_func) % self._m
            if self._counters[number] == 0:
                return False
        return True


bf = BloomFilter(eps=0.01, n=15)
bf.add_element("F")
