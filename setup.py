from setuptools import setup, find_packages  # setup: package banane ke liye, find_packages: auto detect folders
from typing import List  # type hinting ke liye (optional but good practice)

HYPEN_E_DOT = "-e ."  # ye editable install flag hai (requirements.txt me use hota hai)


def get_requirements(file_path: str) -> List[str]:
    """
    Ye function requirements.txt file read karta hai
    aur dependencies ki list return karta hai
    """
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()  # sari lines read karega
        requirements = [req.strip() for req in requirements]  # newline remove karega

        # agar -e . present hai to remove kar denge
        # warna recursion issue ho sakta hai (setup.py khud ko hi call karega)
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements  # final clean list return


setup(
    name="networksecurity",  # project/package ka naam (import me use hoga)
    version="0.0.1",  # versioning (future updates ke liye important)
    author="Omkar",  # tera naam
    packages=find_packages(),  # automatically sare packages (folders) detect karega

    # requirements.txt se dependencies install karega
    install_requires=get_requirements("requirments.txt"),

    python_requires=">=3.8",  # minimum python version define
)