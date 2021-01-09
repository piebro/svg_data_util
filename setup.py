#!/usr/bin/env python

from distutils.core import setup

setup(name='svg_data_util',
      version='0.0.1',
      description='Tool to simplify svgs for machine learning',
      url='https://github.com/piebro/svg_data_util',
      license='MIT',
      author='Piet Brömmel',
      author_email='piet.broemmel@gmail.com',
      setup_requires=['wheel'],
      install_requires=['numpy', 'svgpathtools', 'rdp'],
     )