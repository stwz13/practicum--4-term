from hyperloglog import HyperLogLog
from infinite_str_stream_generation import infinite_str_stream_generation

def test_adding_elements_to_hll():
    count_of_elements = 25
    accuracy = 0.05
    hll = HyperLogLog.make_hpp_with_specified_accuracy(n=count_of_elements, eps=accuracy)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add_element(element)

    assert (hll.get_top_score_of_cardinality() - count_of_elements) / count_of_elements < accuracy

def test_adding_same_elements():
    count_of_elements = 75
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(n=count_of_elements, eps=accuracy)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]
    for element in elements:
        hll.add_element(element)
        hll.add_element(element)

    assert (hll.get_top_score_of_cardinality() - count_of_elements) / count_of_elements < accuracy

def test_adding_small_stream_to_hll():
    count_of_elements = 25000
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(n=count_of_elements, eps=0.05)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add_element(element)

    assert (hll.get_top_score_of_cardinality() - count_of_elements) / count_of_elements < accuracy

def test_adding_normal_stream_to_hll():
    count_of_elements = 250000
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(n=count_of_elements, eps=0.05)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add_element(element)

    assert (hll.get_top_score_of_cardinality() - count_of_elements) / count_of_elements < accuracy

def test_adding_big_stream_to_hll():
    count_of_elements = 10 ** 6
    accuracy = 0.1
    hll = HyperLogLog.make_hpp_with_specified_accuracy(n=count_of_elements, eps=accuracy)

    elements = [next(infinite_str_stream_generation()) for _ in range(count_of_elements)]

    for element in elements:
        hll.add_element(element)

    assert (hll.get_top_score_of_cardinality() - count_of_elements) / count_of_elements < accuracy