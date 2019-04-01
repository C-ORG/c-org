from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import shutil
import os
import sys
sys.path.append("c_org")
from utils import check_files

class PostDevelopCommand(develop):
    """Post-installation for development mode.
    See: https://stackoverflow.com/a/36902139/4986615 """

    def run(self):
        check_files()
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        check_files()
        install.run(self)


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='c_org',
    version='0.1',
    url='https://github.com/C-ORG/c-org',
    long_description=readme(),
    license='GNU GPL',
    author='Pierre-Louis Guhur',
    author_email='pierre-louis.guhur@laposte.net',
    description='Command line tools to derive Continuous Organisations',
    packages=find_packages(exclude=['tests', 'doc']),
    zip_safe=False,
    include_package_data=True,
    install_requires=['PyYaml', 'py-solc', 'web3', 'pytest'],
    entry_points={
        'console_scripts': ['c-org=c_org.cli:main'],
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    # setup_requires=['nose>=1.0'],
    # test_suite='nose.collector'
)
