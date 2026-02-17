import mmh3
import numpy as np
import bitarray



class BloomFilter:
    def __init__(self, k: int = None, m: int = None, eps: float = None , n: int = None):
        if eps is not None and n is not None:
            self.__m = int(np.ceil(-n * np.log(eps) / (np.log(2) ** 2)))
            self.__k = int(np.ceil(self.__m * np.log(2) / n))
        elif k is not None and m is not None:
            self.__m = m
            self.__k = k
        else:
            raise TypeError("Need a pare of parameters k and m or eps and n")
        self.__bite_array = bitarray.bitarray(self.__m)


    def add_to_filter(self, element: str):
        for number_of_hash_func in range(self.__k):
            array_index = self.get_hash(element, number_of_hash_func) % self.__m
            self.__bite_array[array_index] = 1


    @staticmethod
    def get_hash(element: str, number_of_function: int):
        return mmh3.hash128(str(number_of_function) + element) % (2**30)


    def check_element_in_filter(self, element: str):
        for number_of_hash_func in range(self.__k):
            number = self.get_hash(element, number_of_hash_func) % self.__m
            if self.__bite_array[number] == 0:
                return False
        return True


bf = BloomFilter(eps=0.01, n=15)
bf.add_to_filter("F")
