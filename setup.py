from setuptools import setup, find_packages

setup(
    name='dsmr-parser',
    description='Library to parse Dutch Smart Meter Requirements (DSMR)',
    author='Nigel Dokter and many others',
    author_email='mail@nldr.net',
    license='MIT',
    url='https://github.com/ndokter/dsmr_parser',
    version='1.8.0',
    packages=find_packages(exclude=('test', 'test.*')),
    install_requires=[
        'serialx>=1.8,<2',
        'Tailer==0.4.1',
        'dlms_cosem==21.3.2'
    ],
    entry_points={
        'console_scripts': ['dsmr_console=dsmr_parser.__main__:console']
    },
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ]
)
