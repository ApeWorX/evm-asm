#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # type: ignore


extras_require = {
    "cbor": ["cbor==5.2.0"],
    "test": [
        "py-evm==0.3.0a20",
        "pytest==6.2.1",
        "pytest-xdist",
        "pytest-coverage",
        "web3<6.0",
    ],
    "lint": [
        "black==20.8b1",
        "flake8==3.8.4",
        "isort>=5.7.0,<6",
        "mypy==0.790",
        "pydocstyle>=5.1.1,<6",
    ],
    "doc": [
        "Sphinx>=3.4.3,<4",
        "sphinx_rtd_theme>=0.5.1",
    ],
    "ethervm": ["flask", "flask-table", "web3<6.0"],
    "dev": [
        "pytest-watch",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require["test"] = extras_require["test"] + extras_require["cbor"]
extras_require["dev"] = (
    extras_require["dev"]
    + extras_require["test"]  # noqa: W504
    + extras_require["lint"]  # noqa: W504
    + extras_require["doc"]  # noqa: W504
)

with open("./README.md") as readme:
    long_description = readme.read()

setup(
    name="evm-asm",
    version="0.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Shade Undertree",
    author_email="shadeundertree@gmail.com",
    url="https://github.com/ShadeUndertree/evm-asm",
    include_package_data=True,
    python_requires=">=3.6, <4",
    install_requires=[],
    extras_require=extras_require,
    py_modules=["evm_asm"],
    license="Apache License 2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
