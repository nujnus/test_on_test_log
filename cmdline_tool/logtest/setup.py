#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: sunjun
# Mail: 50191646@qq.com
# Created Time:  <datetime: 2019-07-03 22:12:35>  
#############################################
  
from setuptools import setup, find_packages

setup(
    name = "logtest",
    version = "0.1",
    keywords = ("pip", "log","test"),
    description = "test with log",
    long_description = "by comparing the log value and expected value , test the web frontend programme",
    license = "MIT Licence",

    url = "",
    author = "SunJun",
    author_email = "50191646@qq.com",

    packages = ["logtest"],
    include_package_data = True,
    platforms = "any",
    install_requires = [""],
    scripts = ['bin/logtest']
)
