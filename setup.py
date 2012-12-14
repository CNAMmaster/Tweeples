# Setup script for Tweeples.
#
# This file is part of the Tweeples collection of scripts.
#
# Tweeples is free software: you can redistribute it and/or modify it
# under the terms of the BSD license. For the full terms of the license
# see the file `COPYING' in this directory.

from setuptools import setup, find_packages
import sys, os

version = '0.1'

install_requires = [
    # -*- Extra requirements: -*-
    ]

setup(name='tweeples',
      version=version,
      description="A Twitter mining application for people-networks",
      long_description=open("./README.md", "r").read(),
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
          ],
      keywords='Tweeples, Social Media, command-line tools, web 2.0',
      author='Giorgos Keramidas',
      author_email='gkeramidas+tweeples@gmail.com',
      url='https://github.com/GKeramidas/Tweeples',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      tweeples=tweeples:main
      """,
      )
