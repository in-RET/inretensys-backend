from setuptools import find_packages, setup

setup(
    name="InRetEnsys",
    version="0.2a5",
    author="Andreas Lubojanski",
    author_email="andreas.lubojanski@hs-nordhausen.de",
    description="InRetEnsys is a backend to build energysystems from abstract configcontainers for oemof.solph.",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    license="aGPL",
    package_dir={"": "InRetEnsys"},
    packages=find_packages(where=""),
    python_requires=">= 3.7",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License"
        "Operating System :: OS Independent"
    ],
    install_requires=['pydantic', 'oemof.solph>0.4.4', 'pyrsistent']
)
