import string
import random
import pytest
import numpy as np
from typing import Tuple


from bloom_counter_filter import BloomCounterFilter

def generate_random_string(str_len: int):
    return "".join(random.choices(string.ascii_letters + string.digits, k=str_len))
