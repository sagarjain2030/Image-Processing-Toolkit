import numpy as np
from app import process_function1

def test_process_function1_returns_image():
    image = np.array([
        [[10, 20, 30], [40, 50, 60]],
        [[70, 80, 90], [100, 110, 120]]
    ], dtype=np.uint8)
    result = process_function1(image)
    assert np.array_equal(result, image)