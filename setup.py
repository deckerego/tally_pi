#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os

def all_files(newroot, oldroot):
    fdtuples = []
    for root, dirs, files in os.walk(oldroot):
        fds = []
        for fd in files:
            if not fd[0] is '.':
                fds.append(os.path.join(root, fd))
        relpath = os.path.relpath(root, oldroot)
        fdtuple = (os.path.join(newroot, relpath), fds)
        fdtuples.append(fdtuple)
    return fdtuples

base_data_files = [
    ('/etc',    ['etc/tallypi.conf']),
    ('/etc/init.d',    ['etc/init.d/tallypi']),
    ('/etc/default',    ['etc/default/tallypi']),
    ('/usr/share/doc/tallypi', ['README.md', 'LICENSE'])
]

setup(
    name='tallypi',
    version='0.2.1',
    description='A network controlled tally light for video cameras',
    author='DeckerEgo',
    author_email='john@deckerego.net',
    url='http://tallypi.deckerego.net/',
    long_description=open('README.md').read(),
    packages=[
        'tallypi',
        'tallypi.webapp',
    ],
    package_dir={
        '': 'lib'
    },
    data_files=(base_data_files),
    scripts=[
        'scripts/run_server.py'
    ],
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording"
    ],
    keywords='tally light obs raspberry pi rpi cameras video recording',
    requires=[
        'bottle (>=0.12.15)',
        'paste (>=3.0.6)'
    ],
)
