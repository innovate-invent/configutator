from distutils.core import setup

setup(
    name='configutator',
    version='1.0.0',
    packages=['ruamel.yaml', 'jmespath', 'asciimatics'],
    url='https://github.com/innovate-invent/configutator',
    license='MIT License',
    author='Nolan',
    author_email='innovate.invent@gmail.com',
    description='Maps yaml nodes and command line arguments to python function parameters.'
)
