from sklearn.metrics import accuracy_score

from hyperloglog import HyperLogLog
from infinite_str_stream_generation import infinite_str_stream_generation

def test_adding_elements_to_hll():
    count_of_elements = 25

    hll = HyperLogLog(p=8)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - count_of_elements) / count_of_elements < 0.1

def test_adding_same_elements():
    count_of_elements = 75
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(eps=accuracy)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]
    for element in elements:
        hll.add(element)
        hll.add(element)

    assert abs(hll.cardinality() - count_of_elements) / count_of_elements < accuracy

def test_adding_small_stream_to_hll():
    count_of_elements = 25000
    accuracy = 0.1
    hll = HyperLogLog(p=8)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - len(set(elements))) / len(set(elements)) < 3 * accuracy

def test_adding_normal_stream_to_hll():
    count_of_elements = 250000
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(eps=accuracy)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - len(set(elements))) / len(set(elements)) < accuracy

def test_adding_big_stream_to_hll():
    count_of_elements = 10 ** 6

    hll = HyperLogLog.make_hpp_with_specified_accuracy(eps=0.01)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add(element)

    assert abs(hll.cardinality() - len(set(elements))) / len(set(elements)) < 0.01