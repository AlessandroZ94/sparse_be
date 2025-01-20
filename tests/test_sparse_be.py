from sparse_block_encode.utils import create_banded_circulant_matrix
from sparse_block_encode.sparse_be import be
from qiskit import QuantumCircuit
import unittest   # The test framework

class Test_TestMatrix(unittest.TestCase):
    
    def test_matrix(self):
        A = create_banded_circulant_matrix(2, 1, 0.25, 0.5)
        self.assertEqual(A[0,0], 1)
        self.assertEqual(A[0,1], 0.5)
        self.assertEqual(A[1,0], 0.25)

    def test_be(self):
        A = create_banded_circulant_matrix(2, 1, 0.25, 0.5)
        circuit, alpha = be(A)
        self.assertIsInstance(circuit, QuantumCircuit, "Object is not an instance of QuantumCircuit")
        

if __name__ == '__main__':
    unittest.main()
