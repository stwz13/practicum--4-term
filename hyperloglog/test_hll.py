import pytest
from hyperloglog import HyperLogLog
from infinite_str_stream_generation import infinite_str_stream_generation, get_set_of_unique_elements

def test_uncorrected_p():
    with pytest.raises(ValueError):
        HyperLogLog(p=-5)

def test_uncorrected_eps():
    with pytest.raises(ValueError):
        HyperLogLog.make_hpp_with_specified_accuracy(eps=-0.01)
    with pytest.raises(ValueError):
        HyperLogLog.make_hpp_with_specified_accuracy(eps=151)

def test_adding_elements_to_hll():
    count_of_elements = 25

    hll = HyperLogLog(p=8)

    elements = get_set_of_unique_elements(count_of_elements)

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - count_of_elements) / count_of_elements < 0.1

def test_adding_same_elements():
    count_of_elements = 75
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(eps=accuracy)

    elements = get_set_of_unique_elements(count_of_elements)
    for element in elements:
        hll.add(element)
        hll.add(element)

    assert abs(hll.cardinality() - count_of_elements) / count_of_elements < accuracy

def test_adding_small_stream_to_hll():
    count_of_elements = 25000
    accuracy = 0.1
    hll = HyperLogLog(p=8)

    elements = get_set_of_unique_elements(count_of_elements)

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - len(set(elements))) / len(set(elements)) < 3 * accuracy

def test_adding_normal_stream_to_hll():
    count_of_elements = 250000
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(eps=accuracy)

    elements = get_set_of_unique_elements(count_of_elements)

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - len(set(elements))) / len(set(elements)) < 3*accuracy

def test_adding_big_stream_to_hll():
    count_of_elements = 10 ** 6
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(eps=0.01)

    elements = get_set_of_unique_elements(count_of_elements)

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - len(set(elements))) / len(set(elements)) < 3 * accuracy

def test_union_with_diff_p():
    hll1 = HyperLogLog(p=1)
    hll2 = HyperLogLog(p=2)

    with pytest.raises(ValueError):
        hll1 + hll2

def test_union_of_small_and_normal_streams():
    len1 = 25000
    len2 = 250000

    hll1 = HyperLogLog(p=16)
    hll2 = HyperLogLog(p=16)

    elements1 = get_set_of_unique_elements(len1)
    elements2 = get_set_of_unique_elements(len2)

    common_len = len(set(elements1)) + len(set(elements2))

    for element in elements1:
        hll1.add(element)

    for element in elements2:
        hll2.add(element)

    union = hll1 + hll2

    assert (union.cardinality() - common_len) / common_len <= 0.1