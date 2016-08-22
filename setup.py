from setuptools import setup, find_packages

setup(
    name='dsmr-parser',
    description='Library to parse Dutch Smart Meter Requirements (DSMR)',
    author='Nigel Dokter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyserial==3.0.1',
        'pytz==2016.3'
    ]
)
