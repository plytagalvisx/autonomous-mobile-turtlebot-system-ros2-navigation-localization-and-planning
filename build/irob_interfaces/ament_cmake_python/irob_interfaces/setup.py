from setuptools import find_packages
from setuptools import setup

setup(
    name='irob_interfaces',
    version='1.0.0',
    packages=find_packages(
        include=('irob_interfaces', 'irob_interfaces.*')),
)
