import mmh3
import numpy as np
import bitarray



class BloomFilter:
    def __init__(self, k: int, m: int, eps: float = None , n: int = None):
        if (eps is not None and n is not None):
            m = (int)(-n * np.log(eps) / (np.log(2)**2))
            k = (int)(m * np.log(2) / n)
        self.__bite_array = bitarray.bitarray(m)
        self.__k = k
        self.__m = m

    def add_to_filter(self, element: str):
        for i in range(self.__k):
            number = self.__get_hash(str(element), i) % self.__m
            self.__bite_array[number] = 1

    def __get_hash(self, element: str, number_of_function: int):
        return (mmh3.hash128(str(number_of_function) + element) % 2**30)


    def check_element_is_in_filter(self, element: str):
        for i in range(self.__k):
            number = self.__get_hash(element, i) % self.__m
            if self.__bite_array[number] == 0:
                return False
        return True