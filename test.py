import string
import random
import pytest
import numpy as np
from typing import Tuple


from bloom_counter_filter import BloomCounterFilter

def generate_random_string(str_len: int):
    return "".join(random.choices(string.ascii_letters + string.digits, k=str_len))

def test_added_element_is_in_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.1, n=15)
    element = generate_random_string(5)
    bloom_counter_filter.add_element(element)

    assert bloom_counter_filter.element_is_in_filter(element)

def test_unadded_element_is_not_in_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.1, n=15)
    element = generate_random_string(5)

    assert not bloom_counter_filter.element_is_in_filter(element)

def test_delete_element_from_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.1, n=15)

    element = generate_random_string(5)
    bloom_counter_filter.add_element(element)
    bloom_counter_filter.remove_element(element)

    assert not bloom_counter_filter.element_is_in_filter(element)

def test_old_element_is_in_filter_after_delete_another_element():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=15)

    element1 = generate_random_string(5)
    element2 = generate_random_string(5)

    bloom_counter_filter.add_element(element1)
    bloom_counter_filter.add_element(element2)

    bloom_counter_filter.remove_element(element1)

    assert (bloom_counter_filter.element_is_in_filter(element2)
            and not bloom_counter_filter.element_is_in_filter(element1))

def test_add_several_elements_in_filter():
    n = 15
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=n)
    elements_to_add = [generate_random_string(5) for i in range(n)]
    for element in elements_to_add:
        bloom_counter_filter.add_element(element)

    for element in elements_to_add:
        assert bloom_counter_filter.element_is_in_filter(element)

def test_wrong_params():
    with pytest.raises(ValueError):
        BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.01, n = -5)
    with pytest.raises(ValueError):
        BloomCounterFilter.make_filter_with_specified_accuracy(eps=15, n = 5)
    with pytest.raises(ValueError):
        BloomCounterFilter.make_filter_with_specified_accuracy(eps=15, n = -5)
    with pytest.raises(ValueError):
        BloomCounterFilter(k=-5, m=10)
    with pytest.raises(ValueError):
        BloomCounterFilter(k=5, m=-10)
    with pytest.raises(ValueError):
        BloomCounterFilter(k=-5, m=-10)


def test_try_to_remove_element_that_is_not_in_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=15)
    with pytest.raises(ValueError):
        bloom_counter_filter.remove_element("F")


def calculate_false_positive_rate(n: int, eps: float,
                             num_trials: int,
                             per_of_fullness: float) -> Tuple[float, float]:
    results = []
    for _ in range(num_trials):
        bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(n=n, eps=eps)

        num_of_elements_to_add = int(np.ceil(n * per_of_fullness))

        elements_to_add = set()
        while len(elements_to_add) != num_of_elements_to_add:
            elements_to_add.add(generate_random_string(15))

        for element in elements_to_add:
            bloom_counter_filter.add_element(element)

        unadded_elements = set()
        while len(unadded_elements) != num_of_elements_to_add:
            element = generate_random_string(15)
            if element not in elements_to_add:
                unadded_elements.add(element)

        num_of_false_positive_elements = 0
        for element in unadded_elements:
            if bloom_counter_filter.element_is_in_filter(element):
                num_of_false_positive_elements += 1

        results.append(num_of_false_positive_elements/num_of_elements_to_add)

    mean = np.mean(results)
    variance = np.var(results)

    return mean, variance



n_values = (25000, 130000, 750000)
eps_values = (0.7, 0.15, 0.05)
pers_of_fullness = (0.25, 0.5, 0.75, 0.95)

for n, eps in zip(n_values, eps_values):
    for per in pers_of_fullness:
        mean, var = calculate_false_positive_rate(n=n, eps=eps, num_trials=5, per_of_fullness=per)
        k, m = BloomCounterFilter.calculate_k_and_m__with_specified_accuracy(n=n, eps=eps)
        theory_value = (1 - np.exp(-k*n/m)) ** k

        print(f"n: {n}, eps: {eps}, k: {k}, m: {m}, theory_eps: {theory_value}, mean: {mean}, var: {var}")


