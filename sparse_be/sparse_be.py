# Efficient block encoding of certain sparse matrices. Credits to:
# Camps, Daan, et al. "Explicit quantum circuits for block encodings of certain sparse matrices." SIAM Journal on Matrix Analysis and Applications 45.1 (2024): 801-827.
import numpy as np
import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate, MCXGate
from qiskit.circuit.library import UCRYGate


def L_gate_create(j_qubits, reverse_bits=True, draw=False):
    qc = QuantumCircuit(j_qubits, name='L')
    for i in range (0, j_qubits-1):
        gate = MCXGate(j_qubits-1-i)
        l = list(range(i+1, j_qubits))
        l.append(i)
        qc.append(gate, l)
    qc.x(j_qubits-1)
    if reverse_bits:
        qc = qc.reverse_bits()
    if draw:
        qc.draw("mpl", 1, "./images/L_gate.png")
    L_gate = qc.to_gate()
    return L_gate

def R_gate_create(j_qubits, reverse_bits=True, draw=False):
    qc = QuantumCircuit(j_qubits, name='R')
    list_R = list(range(1, j_qubits))
    qc.x(list_R)
    for i in range (0, j_qubits-1):
        gate = MCXGate(j_qubits-1-i)
        l = list(range(i+1, j_qubits))
        l.append(i)
        qc.append(gate, l)
        if i < j_qubits-2:
            qc.x(i+1)
    if reverse_bits:
        qc = qc.reverse_bits()
    if draw:
        qc.draw("mpl", 1, "./images/R_gate.png")
    R_gate = qc.to_gate()
    return R_gate

def be(A, reverse_bits=True, draw=False):
    
    '''
    Block encoding of a banded circulant matrix or a symmetric 2x2 matrix. Returns the Qiskit circuit that
    block encodes A and a float subnormalization factor
    1)  A is the matrix to be block encoded.
    2)  reverse_bits is a boolean variable that when set to True return the circuit using the little
        endian conversion of Qiskit for the j working register
    '''

    # subnormalization factor factor
    epsm = np.finfo(A.dtype).eps
    factor = np.linalg.norm(np.ravel(A), np.inf)
    if factor > 1:
        factor = factor + np.sqrt(epsm)
        A = A/factor
    else:
        factor = 1.0

    n = A.shape[0] # matrix dimension
    j_qubits = int(math.log2(n)) # working qubits
    neg = False

    if(A[0,0] < 0 and j_qubits > 1):
        A = -A
        neg = True

    alpha = A[0,0] # main diagonal term
    beta = A[1,0] # lower diagonal term
    gamma = A[0,1] # upper diagonal term
    set_lower_diag = True
    set_upper_diag = True

    if j_qubits > 1:
        # banded circulant matrix case

        anc_qubits = 3
        # check matrix values and find ancillary qubits number
        if beta == 0:
            anc_qubits = 2
            set_lower_diag = False
        
        if gamma == 0:
            anc_qubits = 2
            set_upper_diag = False

        # circuit definition
        a_reg = QuantumRegister(1, "a")
        l_reg = QuantumRegister(anc_qubits-1, "l")
        j_reg = QuantumRegister(j_qubits, "j")
        circ = QuantumCircuit(a_reg, l_reg, j_reg)

        if neg:
            # add a -1 factor to the overall circuit to block encode the correct matrix
            circ.unitary(-np.eye(2**(j_qubits)), range(anc_qubits,anc_qubits+j_qubits)) 

        circ.h(list(range(1,anc_qubits)))

        #Oa circuit
        value = 1
        if anc_qubits == 2:
            value = 0

        theta0=2*np.arccos(alpha-value)
        theta1=2*np.arccos(beta)
        theta2=2*np.arccos(gamma)

        # Using uniformly controlled rotation
        angles = [theta0, theta1, theta2, 0]
        if beta == 0:
            angles = [theta0, theta2]
        if gamma == 0:
            angles = [theta0, theta1]
        controls = list(range(anc_qubits-1))
        target = [anc_qubits-1]
        circ.append(UCRYGate(angles), controls +  target)

        # Oc circuit
        r1=2
        r2=1

        if (not set_lower_diag) or (not set_upper_diag):
            r1 = 1
            r2 = 1
            
        if set_lower_diag:
            # set the lower diagonal value beta
            j_qubits_spec1 = list(range(anc_qubits, anc_qubits+j_qubits))
            j_qubits_spec1.insert(0, r2)
            circ.append(L_gate_create(j_qubits, reverse_bits, draw).control(1), j_qubits_spec1)

        if set_upper_diag:
            # set the upper diagonal value beta
            j_qubits_spec2 = list(range(anc_qubits, anc_qubits+j_qubits))
            j_qubits_spec2.insert(0, r1)
            circ.append(R_gate_create(j_qubits, reverse_bits, draw).control(1), j_qubits_spec2)

        circ.h(list(range(1,anc_qubits)))

    elif j_qubits==1:
        # symmetric 2x2 matrix case
        anc_qubits = 2
        j_reg = QuantumRegister(j_qubits, "j")
        a_reg = QuantumRegister(anc_qubits, "a")
        circ = QuantumCircuit(a_reg, j_reg)
        circ.h(1)

        #Oa circuit
        theta1 = 2*np.arccos(alpha)
        theta2 = 2*np.arccos(beta)
        RY1 = RYGate(theta1)
        RY2 = RYGate(theta2)
        circ.x(1)
        circ.append(RY1.control(1), [1, 0])
        circ.x(1)
        circ.append(RY2.control(1), [1, 0])

        #Oc circuit
        circ.cx(1,2)
        circ.h(1)

    if draw:
        circ.draw("mpl", 1, "./images/block_encoding.png")
    return circ, factor