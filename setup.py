from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

setup(
    name='TagBit',
    version='1.0',
    url='https://github.com/ModestBitboard/TagBit',
    license='MIT',
    author='Akito Hoshi',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
    ],
    description='A lightweight python library for reading and writing to NFC tags via PC/SC',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    packages=find_packages(include=["tagbit"]),
)
