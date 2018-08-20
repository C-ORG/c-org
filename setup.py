from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='c_org',
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
      install_requires = ['PyYaml', 'py-solc', 'web3'],
      # scripts=['bin/c-org.sh'],
      entry_points={
          'console_scripts': ['c_org=c_org.cli:main'],
      },
      # setup_requires=['nose>=1.0'],
      # test_suite='nose.collector'
      )
