
from setuptools import (
    setup,
    find_packages,
)


setup(
    name='pullenti',
    version='3.13',
    description='Named entity recognition for russian language',
    url='http://pullenti.ru/',
    author='Konstantin Kuznetsov',
    author_email='k.smith@mail.ru',
    license='Free for non-commercial use',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='natural language processing, russian morphology, named entity recognition',
    packages=find_packages(),
    package_data={
        '': [
            '*.png',
            '*.dat',
            '*.txt',
            '*.csv',
            '*.jpg'
        ]
    },
)
