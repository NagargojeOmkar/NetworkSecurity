from setuptools import setup, find_packages  # package setup + auto-detect modules
from typing import List

HYPEN_E_DOT = "-e ."  # editable install flag


def get_requirements(file_path: str) -> List[str]:
    """Read requirements file and return dependency list"""
    requirements = []

    with open(file_path) as file_obj:
        requirements = [req.strip() for req in file_obj.readlines()]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)  # avoid recursive install

    return requirements


setup(
    name="networksecurity",  # package name
    version="0.0.1",
    author="Omkar",
    packages=find_packages(),  # auto-discover packages
    install_requires=get_requirements("requirements.txt"),  # load dependencies
    python_requires=">=3.8",  # minimum Python version
)