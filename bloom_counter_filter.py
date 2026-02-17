from bloom_filter import BloomFilter
import numpy as np

class BloomCounterFilter:
    def __init__(self, k: int, m: int, eps: float = None, n: int = None):
        if eps is not None and n is not None:
            self.__m = np.ceil(-n * np.log(eps) / (np.log(2) ** 2))
            self.__k = np.ceil(self.__m * np.log(2) / n)
        elif k is not None and m is not None:
            self.__k = k
            self.__m = m
        else:
            raise TypeError("Check the arguments")
        self.__counters = [0] * self.__m

    def add_element(self, element: str):
        for number_of_hash_function in range(self.__k):
            count_number = BloomFilter.get_hash(element, number_of_hash_function) % self.__m
            self.__counters[count_number] += 1

    def check_element_in_filter(self, element: str):
        for number_of_hush_function in range(self.__k):
            count_number = BloomFilter.get_hash(element, number_of_hush_function) % self.__m
            if self.__counters[count_number] == 0:
                return False
        return True

    def remove_element(self, element: str):
        if not self.check_element_in_filter(element):
            raise ValueError("Element not in the filter")
        for number_of_hush_function in range(self.__k):
            count_number = BloomFilter.get_hash(element, number_of_hush_function) % self.__m
            self.__counters[count_number] -= 1


