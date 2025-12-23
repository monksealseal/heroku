from setuptools import setup, find_packages

setup(
    name="gcm",
    version="1.0.0",
    description="Sophisticated General Circulation Model with Advanced Physics",
    author="GCM Development Team",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "numba>=0.57.0",
        "matplotlib>=3.7.0",
        "xarray>=2023.1.0",
        "netCDF4>=1.6.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
)
