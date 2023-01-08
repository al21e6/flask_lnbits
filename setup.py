from setuptools import find_packages, setup
from typing import List


def readme() -> str:
    try:
        with open("README.md") as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"{e}")
        return ""


def requirements() -> List[str]:
    try:
        with open("requirements.txt") as f:
            return f.read().split("\n")
    except FileNotFoundError as e:
        print(f"{e}")
        return [""]


setup(
    name="flask_lnbits",
    version="1.0.0",
    description="",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Bitcoin Lightning",
    ],
    url="https://github.com/al21e6/flask_lnbits",
    author="al21e6",
    author_email="git@alex-lewis.me",
    packages=find_packages(exclude=["tests", "test_*"]),
    install_requires=requirements(),
    include_package_data=True,
    zip_safe=False,
)
