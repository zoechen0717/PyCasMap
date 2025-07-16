#!/usr/bin/env python3
"""
Setup script for PyCasMap
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "PyCasMap - Flexible Python Implementation of CasMap"

setup(
    name="pycasmap",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Flexible Python Implementation of CasMap supporting 3-10plex constructs",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pycasmap",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required
    ],
    entry_points={
        "console_scripts": [
            "pycasmap=pycasmap.__main__:main",
        ],
    },
    keywords="bioinformatics, crispr, casmap, sequencing, analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pycasmap/issues",
        "Source": "https://github.com/yourusername/pycasmap",
        "Documentation": "https://github.com/yourusername/pycasmap#readme",
    },
) 