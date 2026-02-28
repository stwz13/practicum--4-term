from hyperloglog import HyperLogLog
from infinite_str_stream_generation import infinite_str_stream_generation

def test_adding_elements_to_hll():
    hll = HyperLogLog.make_hpp_with_specified_accuracy(n=50, eps=0.05)

    elements = [next(infinite_str_stream_generation()) for _ in range(25)]

    for element in elements:
        hll.add_element(element)

    assert hll.get_top_score_of_cardinality() == 25





