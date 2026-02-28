import pytest
from blooms_filter.bloom_filter import BloomFilter
from infinite_str_stream_generation import infinite_str_stream_generation
from bloom_counter_filter import BloomCounterFilter


def test_added_element_is_in_filter():
    bloom_filter = BloomFilter(k=5, m=15)

    element = next(infinite_str_stream_generation())
    bloom_filter.add_element(element)
    assert bloom_filter.element_is_in_filter(element)

def test_not_added_element_is_not_in_filter():
    bloom_filter = BloomFilter(k=5, m=15)

    element1 = next(infinite_str_stream_generation())
    element2 = next(infinite_str_stream_generation())

    bloom_filter.add_element(element1)

    assert bloom_filter.element_is_in_filter(element1)
    assert not bloom_filter.element_is_in_filter(element2)

def test_add_several_elements():
    bloom_filter = BloomFilter(k=5, m=15)
    n = 25

    elements_to_adding = [next(infinite_str_stream_generation()) for _ in range(n)]
    for element in elements_to_adding:
        bloom_filter.add_element(element)

    for element in elements_to_adding:
        assert bloom_filter.element_is_in_filter(element)

def test_remove_element():
    bloom_filter = BloomFilter.make_filter_with_specified_accuracy(n=5, eps=0.01)

    element = next(infinite_str_stream_generation())
    bloom_filter.add_element(element)
    bloom_filter.remove_element(element)

    assert not bloom_filter.element_is_in_filter(element)

def test_try_to_remove_not_added_element():
    bloom_filter = BloomFilter.make_filter_with_specified_accuracy(n=5, eps=0.01)

    element = next(infinite_str_stream_generation())

    with pytest.raises(ValueError):
        bloom_filter.remove_element(element)

def test_add_many_elements():
    n = 50
    bloom_filter = BloomFilter.make_filter_with_specified_accuracy(n = n, eps=0.01)
    elements_to_adding = [next(infinite_str_stream_generation()) for _ in range(n)]

    for element in elements_to_adding:
        bloom_filter.add_element(element)

    for element in elements_to_adding:
        assert bloom_filter.element_is_in_filter(element)

def test_added_element_is_in_counting_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.1, n=15)
    element = next(infinite_str_stream_generation())
    bloom_counter_filter.add_element(element)

    assert bloom_counter_filter.element_is_in_filter(element)

def test_unadded_element_is_not_in_counting_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.1, n=15)
    element = next(infinite_str_stream_generation())

    assert not bloom_counter_filter.element_is_in_filter(element)

def test_delete_element_from_counting_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.1, n=15)

    element = next(infinite_str_stream_generation())
    bloom_counter_filter.add_element(element)
    bloom_counter_filter.remove_element(element)

    assert not bloom_counter_filter.element_is_in_filter(element)

def test_old_element_is_in_counting_filter_after_delete_another_element():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=15)

    element1 = next(infinite_str_stream_generation())
    element2 = next(infinite_str_stream_generation())

    bloom_counter_filter.add_element(element1)
    bloom_counter_filter.add_element(element2)

    bloom_counter_filter.remove_element(element1)

    assert (bloom_counter_filter.element_is_in_filter(element2)
            and not bloom_counter_filter.element_is_in_filter(element1))

def test_add_several_elements_in_counting_filter():
    n = 15
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=n)
    elements_to_add = [next(infinite_str_stream_generation()) for _ in range(n)]
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


def test_try_to_remove_element_that_is_not_in_counting_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=15)
    with pytest.raises(ValueError):
        bloom_counter_filter.remove_element("F")

def test_adding_and_removing_in_counting_filter():
    bloom_counter_filter = BloomCounterFilter.make_filter_with_specified_accuracy(eps=0.5, n=15)
    elements_to_adding = [next(infinite_str_stream_generation()) for _ in range(3)]

    for element in elements_to_adding:
        bloom_counter_filter.add_element(element)

    bloom_counter_filter.remove_element(elements_to_adding[-1])

    assert bloom_counter_filter.element_is_in_filter(elements_to_adding[0])
    assert bloom_counter_filter.element_is_in_filter(elements_to_adding[1])
    assert not bloom_counter_filter.element_is_in_filter(elements_to_adding[-1])

def test_union_counting_filters_with_different_m():
    bf1 = BloomCounterFilter(k=5, m=15)
    bf2 = BloomCounterFilter(k=5, m=5)

    with pytest.raises(ValueError):
        bf1 + bf2


def test_union_counting_filters_with_same_m():
    bf1 = BloomCounterFilter(k=5, m=25)
    bf2 = BloomCounterFilter(k=5, m=25)

    common_elements_to_adding = [next(infinite_str_stream_generation()) for _ in range(3)]
    for element in common_elements_to_adding:
        bf1.add_element(element)
        bf2.add_element(element)

    element_to_first_filter = next(infinite_str_stream_generation())
    element_to_second_filter = next(infinite_str_stream_generation())

    bf1.add_element(element_to_first_filter)
    bf2.add_element(element_to_second_filter)

    union_filter = bf1 + bf2

    for element in common_elements_to_adding:
        assert union_filter.element_is_in_filter(element)

    assert union_filter.element_is_in_filter(element_to_first_filter)
    assert union_filter.element_is_in_filter(element_to_second_filter)


def test_intersect_counting_filters_with_different_m():
    bf1 = BloomCounterFilter(k=15, m=10)
    bf2 = BloomCounterFilter(k=15, m=15)

    with pytest.raises(ValueError):
        BloomCounterFilter.intersect_filters(bf1, bf2)


def test_intersect_counting_filters_with_same_m():
    bf1 = BloomCounterFilter.make_filter_with_specified_accuracy(n=15, eps=0.01)
    bf2 = BloomCounterFilter.make_filter_with_specified_accuracy(n=15, eps=0.01)

    common_elements_to_adding = [next(infinite_str_stream_generation()) for _ in range(3)]
    for element in common_elements_to_adding:
        bf1.add_element(element)
        bf2.add_element(element)

    element_to_first_filter = next(infinite_str_stream_generation())
    element_to_second_filter = next(infinite_str_stream_generation())

    intersect_filter = BloomCounterFilter.intersect_filters(bf1, bf2)

    for element in common_elements_to_adding:
        assert intersect_filter.element_is_in_filter(element)

    assert not intersect_filter.element_is_in_filter(element_to_first_filter)
    assert not intersect_filter.element_is_in_filter(element_to_second_filter)



