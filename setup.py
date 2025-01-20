from setuptools import setup, find_packages

setup(
    name="sparse_be",                # Name of your package
    version="0.1.0",                    # Version number
    description="Python and Qiskit implementation of explicit quantum circuits for block encoding of certain sparse matrices.",  # Short description of the package
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",  # Content type of README.md
    url="https://github.com/AlessandroZ94/sparse_be",  # Project URL
    packages=find_packages(),           # Automatically find and include packages
    install_requires=[
        "numpy>=1.21.0", "qiskit>=1.3.1"               # Add dependencies here
    ],
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',            # Minimum Python version required
)