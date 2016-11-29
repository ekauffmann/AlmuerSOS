#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export COVERAGE_FILE=${CIRCLE_ARTIFACTS:=${DIR}}/.coverage
export COVERAGE_HTML=${CIRCLE_ARTIFACTS:=${DIR}}/coverage

coverage run $DIR/manage.py test --verbosity=2 $@ && coverage html -d $COVERAGE_HTML && coverage report -m
