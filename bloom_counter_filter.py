from bloom_filter import BloomFilter

class BloomCounterFilter(BloomFilter):
    def __init__(self, k : int = None, m: int = None, eps: float = None, n: int = None):
        super().__init__(k, m, eps, n)
        self._counters = [0] * self._m

    def add_element(self, element: str):
        for number_of_hash_func in range(self._k):
            array_index = self._get_hash(element, number_of_hash_func) % self._m
            self._counters[array_index] += 1

    def remove_element(self, element: str):
        if not self.check_element_in_filter(element):
            raise ValueError("Element not in the filter")
        for number_of_hush_function in range(self._k):
            count_number = BloomFilter._get_hash(element, number_of_hush_function) % self._m
            self._counters[count_number] -= 1


