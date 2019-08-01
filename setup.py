from os import path, mkdir
from setuptools import setup, find_packages
from setuptools.command.install import install
import re


here = path.abspath(path.dirname(__file__))


class PostInstallCommand(install):
    default_path = path.join(path.expanduser("~"), ".wtl")
    if not path.exists(default_path):
        mkdir(default_path)


# Version
with open(path.join(here, "wtlogger/_version.py")) as version_file:
    version_match = re.search(
        r"^__version__ = \"(.+)\"", version_file.read().strip(), re.M
    )
if version_match:
    pkg_version = version_match.group(1)
else:
    raise ValueError("Package version not found in file.")


setup(
    name="wtlogger",
    version=pkg_version,
    description="Work Time Logger.",
    long_description="Work Time Logger.",
    url="https://pkonarzewski.github.com",
    author="PKonarzewski",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="time logger work",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "alembic>=1.0,<1.1",
        "pandas>=0.24,<0.25",
        "sqlalchemy>=1.3,<1.4",
        "Click==7.0",
        "pendulum>=2.0,<2.1",
    ],
    entry_points={"console_scripts": ["wtl=wtlogger.cli:main"]},
    # $ pip install -e .[dev]
    extras_require={
        "dev": ["pylint", "mypy", "tox", "black"],
        "installer": ["pyinstaller"],
    },
    python_requires="~=3.6",
    cmdclass={"install": PostInstallCommand},
)
