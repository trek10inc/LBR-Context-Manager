from setuptools import find_packages, setup, Command
from lbr_context import __version__

with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='lbr_context',
    version=__version__,
    description='A context manager for custom resources',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Trek10, Inc',
    author_email='package-management@trek10.com',
    url='https://github.com/trek10inc/LBR-Context-Manager',
    packages=[
        'lbr_context'
    ],
    install_requires=[
        'botocore',
        'requests',
    ],
    license='MIT',
)
