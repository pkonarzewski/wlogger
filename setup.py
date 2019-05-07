from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


setup(
    name='wlogger',
    version='0.0.1',

    description='Work logger.',
    long_description='Work logger.',

    url='https://pkonarzewski.github.com',

    author='PKonarzewski',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    keywords='logger work',
    packages=find_packages(exclude=['tests']),
    install_requires=['alembic>=1.0,<1.1',
                      'pandas>=0.24,<0.25',
                      'sqlalchemy>=1.3,<1.4',
                      ],
    entry_points={
        'console_scripts': [
            'wtl=wtl.cli:main',
        ],
    },

    # $ pip install -e .[dev]
    extras_require={
        'dev': ['pylint']
    },
    python_requires='~=3.6'
)
