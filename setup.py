from setuptools import setup, find_packages

setup(
    name="cdipy",
    version="0.1.10",
    packages=find_packages(),
    install_requires=[
        "aiohttp<3.9.0",
        "pyee<9.0.0",
        "websockets<=10.3"
    ],
    author="Pilate",
    author_email="Pilate@pilate.es",
    description="Interface to the Chrome devtools protocol",
    url="https://github.com/pilate/cdipy"
)
