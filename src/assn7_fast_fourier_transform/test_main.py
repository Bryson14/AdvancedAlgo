from unittest import TestCase
from numpy import array
from main import add_buffer


class Test(TestCase):
    def test_add_buffer(self):
        arr = array([1])

        arr2 = array([1, 2, 3])
        arr2_1 = array([1, 2, 3, 0])

        arr3 = [1,2,3]
        arr3_1 = [1,2,3,0]

        arr4 = array([1,2,3,4,5])
        arr4_1 = array([1,2,3,4,5,0,0,0])

        self.assertTrue((arr == add_buffer(arr)).all())
        self.assertTrue((arr2_1 == add_buffer(arr2)).all())
        self.assertTrue((arr3_1 == add_buffer(arr3)).all())
        self.assertTrue((arr4_1 == add_buffer(arr4)).all())