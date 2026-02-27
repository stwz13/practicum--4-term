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

def test_adding_and_removing():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=15)

    elements_to_adding = [generate_random_string(15) for i in range(3)]

    for element in elements_to_adding:
        bloom_counter_filter.add_element(element)

    bloom_counter_filter.remove_element(elements_to_adding[-1])

    assert bloom_counter_filter.element_is_in_filter(elements_to_adding[0])
    assert bloom_counter_filter.element_is_in_filter(elements_to_adding[1])
    assert not bloom_counter_filter.element_is_in_filter(elements_to_adding[2])

def test_union_with_different_m():
    bf1 = BloomCounterFilter(k=5, m=15)
    bf2 = BloomCounterFilter(k=5, m=5)

    with pytest.raises(ValueError):
        bf1 + bf2


def test_union_with_same_m():
    bf1 = BloomCounterFilter(k=5, m=25)
    bf2 = BloomCounterFilter(k=5, m=25)

    common_elements_to_adding = ["A", "B", "C"]
    for element in common_elements_to_adding:
        bf1.add_element(element)
        bf2.add_element(element)

    bf1.add_element("D")
    bf2.add_element("E")

    union_filter = bf1 + bf2

    for element in common_elements_to_adding:
        assert union_filter.element_is_in_filter(element)

    assert union_filter.element_is_in_filter("D")
    assert union_filter.element_is_in_filter("E")


def test_intersect_with_different_m():
    bf1 = BloomCounterFilter(k=3, m=15)
    bf2 = BloomCounterFilter(k=3, m=5)

    with pytest.raises(ValueError):
        BloomCounterFilter.intersect_filters(bf1, bf2)


def test_intersect_with_same_m():
    bf1 = BloomCounterFilter(k=5, m=15)
    bf2 = BloomCounterFilter(k=5, m=15)

    common_elements_to_adding = ["abc", "ABC", "123"]
    for element in common_elements_to_adding:
        bf1.add_element(element)
        bf2.add_element(element)

    bf1.add_element("str1")
    bf2.add_element("str2")

    intersect_filter = BloomCounterFilter.intersect_filters(bf1, bf2)

    for element in common_elements_to_adding:
        assert intersect_filter.element_is_in_filter(element)

    assert not intersect_filter.element_is_in_filter("D")
    assert not intersect_filter.element_is_in_filter("E")



