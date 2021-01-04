#!/usr/bin/env python

from distutils.core import setup

setup(name='SVGsimplify',
      version='0.0.1',
      description='Tool to simplify svgs',
      url='https://github.com/piebro/svgsimplify',
      license='MIT',
      author='Piet Brömmel',
      author_email='piet.broemmel@gmail.com',
      setup_requires=['wheel'],
      install_requires=['vpype', 'numpy', 'svgpathtools'],
     )