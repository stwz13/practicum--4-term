import string
import random
import pytest

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




