from sparse_be.utils import create_banded_circulant_matrix, print_matrix
from sparse_be.sparse_be import be
from qiskit import QuantumCircuit
import numpy as np
import qiskit.quantum_info as qi
import unittest   # The test framework

class Test_TestBlockEncodedMatrix(unittest.TestCase):
    
    def test_full_be_matrix(self):
        # generate a matrix and block encode it
        n = 2
        N = 2**n
        alpha = 1/2
        beta = 1/8
        gamma = -1/4
        A = create_banded_circulant_matrix(n, alpha, beta, gamma)
        #The block encoding will rescale the matrix by a factor of 1/4
        factor=1/4

        initial_matrix = np.array(A, dtype=complex)
        print("\n")
        print_matrix(initial_matrix,2)
        print("\n")
        circ, alpha = be(A, draw=True)

        op = qi.Operator(circ)
        circ_matrix = op.data
        matrix = circ_matrix[0:N,0:N]
        print_matrix(matrix,2)
        print("\n")

        np.testing.assert_almost_equal(matrix, initial_matrix*factor, decimal=16) # equal matrices up to 16 decimal places

    def test_full_be_matrix_2(self):
        # generate a matrix and block encode it
        n = 1
        N = 2**n
        alpha = 1/2
        beta = 1/8
        gamma = 1/8
        A = create_banded_circulant_matrix(n, alpha, beta, gamma) # symmetric 2x2 case
        #The block encoding will rescale the matrix by a factor of 1/2
        factor=1/2

        initial_matrix = np.array(A, dtype=complex)
        print("\n")

        print("\n")
        circ, alpha = be(A, draw=True)

        op = qi.Operator(circ)
        circ_matrix = op.data
        matrix = circ_matrix[0:N,0:N]
    
        print("\n")

        np.testing.assert_almost_equal(matrix, initial_matrix*factor, decimal=16) # equal matrices up to 16 decimal places

 
if __name__ == '__main__':
    unittest.main()