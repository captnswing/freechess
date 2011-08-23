#-*- coding: utf-8 -*-
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# http://guide.python-distribute.org
# http://packages.python.org/distribute/setuptools.html
setup(
    # provide basic metadata
    name="freechess",
    version=0.8,
    author=u'Frank Hoffsümmer',
    description='django app to import and visualize freechess.org chess PGN files',
    author_email='frank.hoffsummer@gmail.com',
    url='https://bitbucket.org/svtidevelopers/python-utils',
    # install packages, see http://docs.python.org/distutils/setupscript.html#listing-whole-packages
    package_dir={'': 'src'},
    packages=find_packages('src'),
    # include all non-python files under source control, e.g. media/ and templates/ directories
    include_package_data=True,
    # make setuptools work with mercurial, see http://pypi.python.org/pypi/setuptools_hg
    setup_requires=["distribute", "setuptools_hg"],
    # install dependencies
    install_requires=[
        'django == 1.3',
        'mysql-python',
        'django-piston',
        # libraries for testing
        'nose',
        'coverage',
        'django-nose',
        'unittest2'
    ],
)
