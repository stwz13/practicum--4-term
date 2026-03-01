import numpy as np
from hashlib import md5
class CountMinSketch:
    def __init__(self, d: int, w: int):
        if w <= 0 or d <= 0:
            raise ValueError("D and w must be higher than 0")

        self._w = w
        self._d = d
        self._matrix = np.zeros((self._d, self._w), dtype=np.uint32)

    @property
    def w(self):
        return self._w

    @property
    def d(self):
        return self._d

    @classmethod
    def make_sketch_with_accuracy(cls, eps: float, delta: float):
        if eps <= 0 or delta <= 0 or delta >= 1:
            raise ValueError("eps > 0 and 0 < delta < 1 required")

        w = int(np.ceil(np.e / eps))
        d = int(np.ceil(np.log(1 / delta)))

        return cls(d, w)

    def add(self, element: str) -> None:
        for i in range(self._d):
            ind = self._get_hash(element, i)
            self._matrix[i, ind] += 1

    def _get_hash(self, element: str, seed: int) -> int:
        hash_value = int.from_bytes(md5((element + str(seed)).encode('utf-8')).digest(), byteorder='big')
        return hash_value % self._w

    def estimate(self, element: str) -> int:
        counts = [self._matrix[i, self._get_hash(element, i)] for i in range(self._d)]
        return min(counts)
