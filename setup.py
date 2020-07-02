from setuptools import setup, find_packages

setup(
    name="cdipy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.5.1", 
        "pyee==7.0.2",
        "websockets==8.1"
    ],
    author="Pilate",
    author_email="Pilate@pilate.es",
    description="Interface to the Chrome devtools protocol",
    url="https://github.com/pilate/cdipy"
)
