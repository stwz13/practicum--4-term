from hashlib import md5
import numpy as np
from infinite_str_stream_generation import infinite_str_stream_generation


class HyperLogLog:
    def __init__(self, n: int, p: int, q: int = 32):
        if n <= 0 or p <= 0:
            raise ValueError("N and p must be positive")

        self._n = n # максимальный размер множества
        self._p = p # количество бит, определяющих разбиение на подмножества
        self._m = 2 ** p# количество счетчиков
        self._q = q# размер счетчиков
        self._registers = [0] * self._m

    @classmethod
    def make_hpp_with_specified_accuracy(cls, n: int, eps: float):
        if not 0 <= eps <= 100:
            raise ValueError("Eps must be less than 100 and higher than 0")
        eps = eps / 100
        p = int(np.ceil(2*np.log2(1.04 / eps)))

        return cls(n, p)

    def add_element(self, element: str) -> None:
        byte_str = element.encode("utf-8")
        x = int(md5(byte_str).hexdigest(), 16)

        j = (x >> (self._q - self._p)) & ((1 << self._p) - 1)
        w = x & ((1 << (self._q - self._p)) - 1)

        if w == 0:
            p_w = self._q - self._p + 1
        else:
            p_w = (self._q - self._p) - w.bit_length() + 1
        self._registers[j] = max(self._registers[j], p_w)

    def get_top_score_of_cardinality(self) -> int:
        count_of_zero_registers = 0
        z = 0
        for reg in self._registers:
            if reg == 0:я
                count_of_zero_registers += 1
            z += 2 ** (-reg)

        score = self._get_alfa() * self._m ** 2 * z

        if count_of_zero_registers > 0 and score < 5/2 * self._m:
            return int(self._m * np.log(self._m / count_of_zero_registers))

        if score > 2 ** self._q / 30:
            return int(-2**32 * np.log(1 - score/2**32))

        return int(score)

    def _get_alfa(self):
        m = self._m
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / m)

    def __add__(self, other):
        if self._p != other._p or self._q != other._q:
            raise ValueError("P and q must have same values")

        union_hpp = HyperLogLog(self._n, self._p, self._q)
        for i in range(self._m):
            union_hpp._registers[i] = max(self._registers[i], other._registers[i])
        return union_hpp


hll = HyperLogLog.make_hpp_with_specified_accuracy(n=50, eps=0.05)

elements = [next(infinite_str_stream_generation()) for _ in range(25)]

for element in elements:
    hll.add_element(element)

hll.get_top_score_of_cardinality()