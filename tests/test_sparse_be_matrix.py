from sparse_be.utils import create_banded_circulant_matrix, print_matrix
from sparse_be.sparse_be import be
from qiskit import QuantumCircuit
import numpy as np
import qiskit.quantum_info as qi
import unittest   # The test framework

class Test_Be_Matrix(unittest.TestCase):
    
    def test_matrix(self):
        # generate a matrix and block encode it
        n = 2
        N = 2**n
        alpha = 1/2
        beta = 1/8
        gamma = -1/4
        A = create_banded_circulant_matrix(n, alpha, beta, gamma)
        #print(A)
        circ, alpha = be(A, reverse_bits=False, draw=True)

        op = qi.Operator(circ.reverse_bits())
        matrix = op.data
        print(matrix)

        self.assertTrue(np.array_equal(matrix, block))

 
if __name__ == '__main__':
    unittest.main()