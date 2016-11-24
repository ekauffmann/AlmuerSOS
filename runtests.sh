#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

coverage run $DIR/manage.py test --verbosity=2 $@ && coverage html && coverage report -m
