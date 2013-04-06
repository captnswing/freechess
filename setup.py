#-*- coding: utf-8 -*-
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# http://guide.python-distribute.org
# http://packages.python.org/distribute/setuptools.html
setup(
    # provide basic metadata
    name="freechess",
    version=1.0,
    author=u'Frank Hoffsümmer',
    description='django app to import and visualize freechess.org chess PGN files',
    author_email='frank.hoffsummer@gmail.com',
    url='https://bitbucket.org/captnswing/freechess',
    # install packages, see http://docs.python.org/distutils/setupscript.html#listing-whole-packages
    package_dir={'': '.'},
    packages=find_packages('.'),
    # include all non-python files under source control, e.g. media/ and templates/ directories
    include_package_data=True,
    # make setuptools work with mercurial, see http://pypi.python.org/pypi/setuptools_hg
    setup_requires=["distribute", "setuptools_hg"],
    # install dependencies
    install_requires=[
        'django>=1.5',
        'mysql-python',
        'psycopg2',
        'dj_database_url'
        # libraries for testing
        'nose',
        'coverage',
        'django-nose',
        'unittest2'
    ],
)
