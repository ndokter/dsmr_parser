from setuptools import setup, find_packages

setup(
    name='dsmr-parser',
    description='Library to parse Dutch Smart Meter Requirements (DSMR)',
    author='Nigel Dokter and many others',
    author_email='nigel@nldr.net',
    url='https://github.com/ndokter/dsmr_parser',
    version='0.29',
    packages=find_packages(exclude=('test', 'test.*')),
    install_requires=[
        'pyserial>=3,<4',
        'pyserial-asyncio<1',
        'pytz',
        'Tailer==0.4.1'
    ],
    entry_points={
        'console_scripts': ['dsmr_console=dsmr_parser.__main__:console']
    },
)
