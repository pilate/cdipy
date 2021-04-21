from setuptools import setup, find_packages

setup(
    name="cdipy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp<3.8.0",
        "pyee==5.0.0",
        "websockets<8.2"
    ],
    author="Pilate",
    author_email="Pilate@pilate.es",
    description="Interface to the Chrome devtools protocol",
    url="https://github.com/pilate/cdipy"
)
