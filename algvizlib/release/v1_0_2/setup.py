#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from setuptools import setup

setup(
    name="algviz",
    version="1.0.2",
    author="zjl9959",
    author_email="zjluestc@outlook.com",
    description=("This is a algorithm visualizer lib."),
    license="GPLv3",
    keywords="Algorithm Visualizer Animation",
    #url="",
    packages=['algviz'],
    install_requires=[
        'graphviz>=0.13.2',
    ],
    classifiers=[
        "Development Status :: 20200528_beta",
        "Topic :: BasicDataAnimation",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=False
)
