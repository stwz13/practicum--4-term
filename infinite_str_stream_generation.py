import string
import random
def infinite_str_stream_generation(max_length = 10, min_length = 1, alf = string.ascii_letters + string.digits + string.punctuation):
    while True:
        length_of_str = random.randint(min_length, max_length)
        yield "".join(random.choices(alf, k=length_of_str))


def get_set_of_unique_elements(n: int):
    unique_elements = set()
    while len(unique_elements) != n:
        unique_elements.add(next(infinite_str_stream_generation()))

    return unique_elements