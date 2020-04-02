from unittest import TestCase
import project_code.src.assn8_poly_multiply_fft.poly_multiply as poly
import numpy as np


class Test(TestCase):
    def test_pad_printout(self):
        # input of strings
        self.assertTrue(poly.pad_printout("1234567890") == "1234567890")
        self.assertTrue(poly.pad_printout("1") == "0000000001")
        self.assertTrue(poly.pad_printout("") == "0000000000")
        self.assertTrue(poly.pad_printout("12345") == "0000012345")

        # input of ints
        self.assertTrue(poly.pad_printout(1234567890) == "1234567890")
        self.assertTrue(poly.pad_printout(1) == "0000000001")
        self.assertTrue(poly.pad_printout(0) == "0000000000")
        self.assertTrue(poly.pad_printout(12345) == "0000012345")

        # input of lists or numpy array
        a = np.array([1, 2, 3, 4])
        a_sol = "0000000001, 0000000002, 0000000003, 0000000004"

        b = [1543, 8467, 515484654, 6874655, 1, 15]
        b_sol = "0000001543, 0000008467, 0515484654, 0006874655, 0000000001, 0000000015"
        self.assertTrue(poly.pad_printout(b) == b_sol)

        b = ['1543', '8467', '515484654', '6874655', '1', '15']
        b_sol = "0000001543, 0000008467, 0515484654, 0006874655, 0000000001, 0000000015"
        self.assertTrue(poly.pad_printout(b) == b_sol)

        # unknown input type
        self.assertTrue(poly.pad_printout({1, 2, 3, 4, 5}) is None)

