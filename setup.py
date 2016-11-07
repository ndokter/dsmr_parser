from setuptools import setup, find_packages

setup(
    name='dsmr-parser',
    description='Library to parse Dutch Smart Meter Requirements (DSMR)',
    author='Nigel Dokter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.2.1',
        'pytz'
    ],
    entry_points={
        'console_scripts': ['dsmr_console=dsmr_parser.__main__:console']
    },
)
