#!/usr/bin/env python3
"""
A setuptools based setup module for the Pumpkin MCU API.
See:
https://github.com/pypa/sampleproject
"""

from setuptools import setup

setup(name='imu',
      version='0.1.5',
      description='KubOS API for communicating with IMU',
      py_modules=["imu_api"],
      install_requires=[
          'i2c'
      ]
      )
