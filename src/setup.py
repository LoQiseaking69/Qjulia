from setuptools import setup, find_packages
from setuptools_rust import RustExtension, Binding

setup(
    name="q_julia",
    version="0.2.0",
    author="Ant OG",
    author_email="Reel0112358.13@proton.me",
    description="Quantum Fractal Generator - A Rust library for generating fractals with quantum-inspired algorithms.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LoQiseaking69/q_julia",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Rust",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="quantum fractals rust python extension pyo3",
    packages=find_packages(),
    rust_extensions=[
        RustExtension(
            "q_julia.q_julia", 
            path="Cargo.toml", 
            binding=Binding.PyO3, 
            native=True, 
            strip=False
        )
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        'PyQt5',
        'numpy',
        'matplotlib'
    ],
    setup_requires=["setuptools-rust"],
)
