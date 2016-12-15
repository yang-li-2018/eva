#!/bin/bash

python3 setup.py sdist
docker build -t ooclab/eva .
