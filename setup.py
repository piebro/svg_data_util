#!/usr/bin/env python

from distutils.core import setup

setup(name='SVGsimplify',
      version='0.0.1',
      description='Tool to simplify svgs',
      author='Piet Brömmel',
      author_email='piet.broemmel@gmail.com',
      url='https://github.com/piebro/svgsimplify',
      packages=['vpype', 'numpy', 'pickle', 'svgpathtools'],
     )