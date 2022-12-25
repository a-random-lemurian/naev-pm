from setuptools import setup

setup(
    name="naev-pm",
    version="0.1.0",
    description="Naev Package Manager",
    author="Lemuria",
    py_modules=['naevpm'],
    install_requires=[
        'Click', 'pygit2'
    ],
    entry_points='''
        [console_scripts]
        naevpm=naevpm:cli.root
    '''
)
