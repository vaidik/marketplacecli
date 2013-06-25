#!/usr/bin/env python

import os

from setuptools import setup, find_packages


def local_file(fn):
    return open(os.path.join(os.path.dirname(__file__), fn))

setup(name='marketplacecli',
      version='0.0.1',
      description='',
      long_description=local_file('README.md').read(),
      author='Vaidik Kapoor',
      author_email='kapoor.vaidik@gmail.com',
      license='',
      url='https://github.com/vaidik/marketplacecli',
      include_package_data=True,
      classifiers=[],
      entry_points="""
        [console_scripts]
        marketplacecli=marketplacecli:main
        """,
      packages=find_packages(),
      install_requires=[ln.strip() for ln in
                        local_file('requirements.txt')
                        if not ln.startswith('#') and
                        not ln.startswith('-e')])
