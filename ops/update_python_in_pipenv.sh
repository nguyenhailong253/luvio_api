#!/bin/bash

# Ref: https://github.com/pypa/pipenv/issues/2482
pipenv --rm
pipenv --python 3.x # replace x with latest version
pipenv install