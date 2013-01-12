try:
    from setuptools import setup, find_packages
except ImporterError:
    from ez_setup import use_setuptools #@UnresolvedImport
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='ssrf',
    version="0.1.0",
    #description='',
    #author='',
    #author_email='',
    #url='',
    install_requires=['nose', 'mox'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector'
)
