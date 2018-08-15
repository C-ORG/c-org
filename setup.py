from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='derive',
      version='0.1',
      url='https://github.com/C-ORG/derive',
      long_description=readme(),
      license='GNU GPL',
      author='Pierre-Louis Guhur',
      author_email='pierre-louis.guhur@laposte.net',
      description='Derive Continuous Organisation',
      packages=find_packages(exclude=['tests', 'examples', 'doc']),
      zip_safe=False,
    #   install_requires = ['psutil']
      setup_requires=['nose>=1.0'],
      test_suite='nose.collector'
      )
