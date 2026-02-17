import BloomFilter


class BloomCounterFilter(BloomFilter):
    def add_to_filter(self, element: str):
        for i in range(self.__k):
            number = self.__get_hash(str(element), i) % self.__m
            self.__bite_array[number] = 1

