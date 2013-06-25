#!/usr/bin/python
'''installation script to install the redrovor package'''

from distutils.core import setup

setup(name="RedROVOR",
    version="0.2.0",
    description="Automated Reduction software designed for the ROVOR observatory",
    author="Thayne McCombs",
    author_email="astrothayne@gmail.com",
    url="https://github.com/tmccombs/RedROVOR",
    packages=['redrovor','redrovor.photometry'],
    )
