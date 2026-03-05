import os
import shutil
import sys
import glob
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import re
with open('socru/__init__.py') as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)

setup(
    name='socru',
    version=version,
    description='socru: genome arrangement types',
	long_description=read('README.md'),
    packages = find_packages(),
    author='Andrew J. Page',
    author_email='andrew.page@quadram.ac.uk',
    url='https://github.com/quadram-institute-bioscience/socru',
    scripts=glob.glob('scripts/*'),
    python_requires='>=3.8',
    install_requires=[
           'biopython >= 1.78',
           'PyYAML',
           'numpy',
           'matplotlib'
       ],
    package_data={'socru': ['data/*', 'data/*/*']},
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)
