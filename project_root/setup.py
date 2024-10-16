# Filename: setup.py\n# Path: project_root/setup.py\n# Log Level: INFO\n
from setuptools import setup, find_packages

setup(
    name='framework',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'run_app = app.main:main',
        ],
    },
)

