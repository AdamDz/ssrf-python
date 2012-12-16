try:
    from setuptools import setup, find_packages
except ImporterError:
    from ez_setup import use_setuptools #@UnresolvedImport
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='openmemo',
    version="0.0.1",
    #description='',
    #author='',
    #author_email='',
    #url='',
    install_requires=['nose', 'mox', 'enum', 'fs>=0.4.0'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector'
)
