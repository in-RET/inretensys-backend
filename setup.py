from setuptools import setup, find_packages

setup(
    name="InRetEnsys",
    version="0.2a1",
    author="Andreas Lubojanski",
    author_email="andreas@lubojanski.com",
    description="InRetEnsys is a backend to build an webinterface for oemof.solph.",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">= 3.8",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License"
        "Operating System :: OS Independent"
    ],
    install_requires=['pydantic', 'oemof.solph']
)
