#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
GIT_ROOT=$(git rev-parse --show-toplevel)
NOT_IN_VENV=`type deactivate &>/dev/null`

$("${GIT_ROOT}/.sh/create_venv.sh")

# create virtual environment if not already in one
if [ NOT_IN_VENV ]; then
    source "${GIT_ROOT}/.venv/bin/activate"
fi

cd "${GIT_ROOT}"

python3 -m pip install --upgrade pip wheel
pip install -e .[test]

pytest
pylint ./dir
bandit -v -r ./dir -f json -o reports/bandit/report.json

cd "${CURRENT_DIR}"

# exit venv if was not previously within one
if [ NOT_IN_VENV ]; then
    deactivate
fi