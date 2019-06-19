from os import path
from setuptools import setup, find_packages
import re


here = path.abspath(path.dirname(__file__))

# Version
with open(path.join(here, 'wtlogger\_version.py')) as version_file:
    version_line = version_file.read().strip()

pkg_version = re.search(r"^__version__ = \"(.+)\"", version_line, re.M).group(1)


setup(
    name='wtlogger',
    version=pkg_version,

    description='Work Time Logger.',
    long_description='Work Time Logger.',

    url='https://pkonarzewski.github.com',

    author='PKonarzewski',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    keywords='time logger work',
    packages=find_packages(exclude=['tests']),
    install_requires=['alembic>=1.0,<1.1',
                      'pandas>=0.24,<0.25',
                      'sqlalchemy>=1.3,<1.4',
                      'Click==7.0'
                      ],
    entry_points={
        'console_scripts': [
            'wtl=wtlogger.cli:main',
        ],
    },

    # $ pip install -e .[dev]
    extras_require={
        'dev': ['pylint', 'mypy', 'tox']
    },
    python_requires='~=3.6'
)
