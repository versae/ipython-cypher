from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1.0'

install_requires = [
    "neo4jrestclient",
    'prettytable',
    'ipython>=1.0',
    'six',
]


setup(
    name='ipython-cypher',
    version=version,
    description="Neo4j Cypher cell magic for IPython and Pandas",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GPL',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
    keywords='ipython neo4j cypher pandas neo4jrestclient',
    author='Javier de la Rosa',
    author_email='versae@gmail.com',
    url='https://github.com/versae/ipython-cypher',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
