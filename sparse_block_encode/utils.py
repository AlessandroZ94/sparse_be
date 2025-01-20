import numpy as np

def tridiag(a, b, c, k1=-1, k2=0, k3=1):
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

def create_banded_circulant_matrix(n, alpha, beta, gamma):
    N = 2**n
    ld = beta*np.ones(N-1)
    md = alpha*np.ones(N)
    ud = gamma*np.ones(N-1)
    A = tridiag(ld, md, ud)
    A[N-1,0]=gamma
    A[0,N-1]=beta
    return A

def print_matrix(matrix, num_qubits):
    for i in range(2**num_qubits):
        print("\n[", end="")
        for j in range(2**num_qubits):
            print(round(np.real(matrix[i,j]),5), end=" ")
        print("]")