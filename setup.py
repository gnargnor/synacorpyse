from setuptools import setup, find_packages

setup(
    name='Synacorpyse',
    version='0.1.0',
    description='Synacor Challenge - Python VM',

    author='Logan Kelly',
    author_email='logankelly@protonmail.com',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[
        'click==7.0'
    ],
    entry_points={
        'console_scripts': [
            'read-binary = read_binary.__main__:main',
        ]
    }
)
