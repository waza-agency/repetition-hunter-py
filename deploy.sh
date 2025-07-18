#!/bin/bash

python -m build
pip install -e .
python -m twine upload dist/*
