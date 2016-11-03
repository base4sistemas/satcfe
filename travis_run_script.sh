#!/usr/bin/env bash

set -e

if [ "${TEST}" != "0" ]; then
    python setup.py test -a "-rs --skip-funcoes-sat"
    exit 0
fi

if [ "${FLAKE}" != "0" ]; then
    bin/python setup.py flake8
    exit 0
fi

if [ "${LINT}" != "0" ]; then
    bin/python setup.py lint
    exit 0
fi

set +e
