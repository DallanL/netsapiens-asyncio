from setuptools import setup, find_packages

setup(
    name="netsapiens-asyncio",
    version="0.1.1",
    description="Asynchronous Python client library for the Netsapiens PBX API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dallan Loomis",
    author_email="Dallan@wedophones.com",
    url="https://github.com/DallanL/netsapiens-asyncio.git",
    packages=find_packages(),
    install_requires=["aiohttp"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
