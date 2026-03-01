from infinite_str_stream_generation import infinite_str_stream_generation
from count_min_sketch import CountMinSketch
import pytest



def test_uncorrected_params():
    with pytest.raises(ValueError):
        CountMinSketch(d=-5, w=-10)
    with pytest.raises(ValueError):
        CountMinSketch.make_sketch_with_accuracy(eps=0.01, delta=15)

def test_no_adding_element():
    sketch = CountMinSketch(d=4, w=100)
    el = next(infinite_str_stream_generation())

    assert sketch.estimate(el) == 0

def test_adding_element():
    sketch = CountMinSketch(d=4, w=100)
    el = next(infinite_str_stream_generation())

    sketch.add(el)
    sketch.add(el)
    sketch.add(el)

    assert sketch.estimate(el) == 3

def test_element_was_not_added_to_sketch():
    sketch = CountMinSketch(d=4, w=100)
    el = next(infinite_str_stream_generation())

    sketch.add(el)
    sketch.add(el)
    sketch.add(el)

    unadded_el = next(infinite_str_stream_generation())
    assert sketch.estimate(el) == 3 and sketch.estimate(unadded_el) == 0

def test_adding_several_elements():
    sketch = CountMinSketch(d=4, w=100)
    el1 = next(infinite_str_stream_generation())
    el2 = next(infinite_str_stream_generation())

    sketch.add(el1)
    sketch.add(el2)
    sketch.add(el2)

    assert sketch.estimate(el1) == 1 and sketch.estimate(el2) == 2

def test_adding_popular_element():
    sketch = CountMinSketch.make_sketch_with_accuracy(eps=0.01, delta=0.1)
    popular_element = next(infinite_str_stream_generation())

    for _ in range(500):
        sketch.add(next(infinite_str_stream_generation()))

    for _ in range(250):
        sketch.add(popular_element)

    assert sketch.estimate(popular_element) >= 250

def test_adding_norm_stream():
    n = 250000

    sketch = CountMinSketch.make_sketch_with_accuracy(eps=0.005, delta=0.05)

    element = next(infinite_str_stream_generation())
    count_of_element = 10000

    for _ in range(n):
        sketch.add(next(infinite_str_stream_generation()))

    for _ in range(count_of_element):
        sketch.add(element)

    assert abs(sketch.estimate(element)  - count_of_element) / count_of_element <= 0.4

def test_adding_big_stream():
    n = 10 ** 6

    sketch = CountMinSketch.make_sketch_with_accuracy(eps=0.005, delta=0.01)

    element = next(infinite_str_stream_generation())
    count_of_element = 10000

    for _ in range(n):
        sketch.add(next(infinite_str_stream_generation()))

    for _ in range(count_of_element):
        sketch.add(element)

    assert abs(sketch.estimate(element) - count_of_element) / count_of_element <= 0.4