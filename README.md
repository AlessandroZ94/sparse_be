# sparse_be
Python and Qiskit implementation of explicit quantum circuits for block encoding of certain sparse matrices.
This implementation is based on the following work: 

Camps, Daan, et al. "Explicit quantum circuits for block encodings of certain sparse matrices (2022)." arXiv preprint arXiv:2203.10236.

Installation guide:
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install .\dist\sparse_be-0.1.0-py3-none-any.whl

Usage guide:
from sparse_be.sparse_be import be

# Create A matrix ...
circuit, alpha = be(A)

