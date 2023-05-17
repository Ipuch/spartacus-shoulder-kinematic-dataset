""" Setup.py file """
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="shoulder",
    version="0.0.1",
    author="Ipuch, ANaaim, FMoissenet",
    author_email="",
    description="Shoulder dataset treatment",
    long_description=long_description,
    packages=[".", "shoulder", "examples", "shoulder/dataset"],
    python_requires=">=3.10",
    zip_safe=False,
)
