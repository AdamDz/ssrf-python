try:
    from setuptools import setup, find_packages
except ImporterError:
    from ez_setup import use_setuptools #@UnresolvedImport
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='ssrf',
    version='0.1.5',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    license='Creative Commons Attribution-Share Alike license',
    description="Simple Spaced Repetition Formula",
    long_description="""
    Simple yet powerful spaced repetition algorithm used by RapidStudy.com.
    See: http://www.rapidstudy.com
    """,
    install_requires=[],
    tests_require=[],
    author='Adam Dziendziel',
    author_email='adam.dziendziel@gmail.com',
    url='https://github.com/AdamDz/ssrf-python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Education',
    ],
)

