# Copyright (C) 2016  Semenovsky, Oleg <o.semenovsky@gmail.com>
# Author: Semenovsky, Oleg <o.semenovsky@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__),
'README.rst')) as readme:
    README = readme.read()

setup(
    name='oshlex',
    version='0.0.1.5',
    packages=['oshlex'],
    license='GNU General Public License v2 (GPLv2)',
    description='Rule based unix-style config parser written with shlex',
    url='https://github.com/osemenovsky/oshlex',
    author='Oleg Semenovsky',
    author_email='o.semenovsky@gmail.com',
    maintainer='Oleg Semenovsky',
    maintainer_email='o.semenovsky@gmail.com',
    long_description=README,
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
