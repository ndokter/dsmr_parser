from setuptools import setup, find_packages

setup(
    name='dsmr-parser',
    description='Library to parse Dutch Smart Meter Requirements (DSMR)',
    author='Nigel Dokter',
    author_email='nigeldokter@gmail.com',
    url='https://github.com/ndokter/dsmr_parser',
    version='0.12',
    packages=find_packages(),
    install_requires=[
        'pyserial>=3,<4',
        'pyserial-asyncio<1',
        'pytz',
        'PyCRC>=1.2,<2'
    ],
    entry_points={
        'console_scripts': ['dsmr_console=dsmr_parser.__main__:console']
    },
)
