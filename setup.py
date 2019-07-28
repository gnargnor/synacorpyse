from setuptools import setup, find_packages

install_requires = [
    'click==7.0',
]

tests_require = [
    'pytest==5.0.1'
]

setup(
    name='Synacorpyse',
    version='0.1.0',
    description='Synacor Challenge - Python VM',

    author='Logan Kelly',
    author_email='logankelly@protonmail.com',

    packages=find_packages(),

    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'synacorpyse = synacorpyse.__main__:main',
        ]
    }
)
