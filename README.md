# sparse_be
Python and Qiskit implementation of explicit quantum circuits for block encoding of certain sparse matrices.
Currently works for banded circulant matrices and symmetric 2x2 matrices.
This implementation is based on the following article: 

Camps, Daan, et al. "Explicit quantum circuits for block encodings of certain sparse matrices (2022)." arXiv preprint arXiv:2203.10236.

# Installation guide:

pip install setuptools wheel

python setup.py sdist bdist_wheel

pip install .\dist\sparse_be-0.1.0-py3-none-any.whl

# Usage guide:

from sparse_be.sparse_be import be
from sparse_be.utils import create_banded_circulant_matrix

A = create_banded_circulant_matrix(2, 1, 0.25, 0.5)
circuit, alpha = be(A)

