from hashlib import md5
import numpy as np
from infinite_str_stream_generation import infinite_str_stream_generation


class HyperLogLog:
    def __init__(self, p: int, q: int = 32):
        if p <= 0:
            raise ValueError("p must be positive")

        self._p = p # количество бит, определяющих разбиение на подмножества
        self._m = 2 ** p# количество счетчиков
        self._q = q# размер счетчиков
        self._registers = [0] * self._m

    @property
    def m(self) -> int:
        return self._m

    @property
    def p(self) -> int:
        return self._p

    @classmethod
    def make_hpp_with_specified_accuracy(cls, eps: float):
        if not 0 <= eps <= 1:
            raise ValueError("Eps must be less than 1 and higher than 0")

        p = int(np.ceil(2*np.log2(1.04 / eps)))

        return cls(p)

    def add(self, element: str) -> None:
        h = int.from_bytes(md5(element.encode('utf-8')).digest(), byteorder='big')
        bucket = h >> (128 - self._p)

        remaining_bits = min(self._q, 128 - self._p)
        w = h & ((1 << remaining_bits) - 1)

        if w == 0:
            count_of_main_zeros = remaining_bits + 1
        else:
            count_of_main_zeros = remaining_bits - w.bit_length() + 1

        self._registers[bucket] = max(self._registers[bucket], count_of_main_zeros)


    def cardinality(self):
        count_of_zero_registers = 0
        z = 0

        for reg in self._registers:
            if reg == 0:
                count_of_zero_registers += 1
            z += 2 ** (-reg)

        z = z ** (-1)
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

        union_hpp = HyperLogLog(self._p, self._q)
        for i in range(self._m):
            union_hpp._registers[i] = max(self._registers[i], other._registers[i])
        return union_hpp
