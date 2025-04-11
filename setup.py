from setuptools import setup, find_packages

setup(
    name="organization",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "asyncio",
    ],
    python_requires=">=3.7",
) 