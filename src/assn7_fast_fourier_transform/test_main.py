from unittest import TestCase
from numpy import array, fft, allclose
from FFT import add_buffer, my_fft, fft_helper


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


    def test_my_fft(self):
        arr1 = array([0,1,2,3,4,5,6,7])
        arr2 = array([5,1,3,4])
        arr3 = array([0])

        self.assertTrue(allclose(fft.fft(arr1), fft_helper(arr1, my_fft)))
        self.assertTrue(allclose(fft.fft(arr2), fft_helper(arr2, my_fft)))
        self.assertTrue(allclose(fft.fft(arr3), fft_helper(arr3, my_fft)))