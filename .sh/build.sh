#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
GIT_ROOT=$(git rev-parse --show-toplevel)
NOT_IN_VENV=`type deactivate &>/dev/null`

$("${GIT_ROOT}/.sh/create_venv.sh")

# if not in a python virtual environment
if [ NOT_IN_VENV ]
then
    source "${GIT_ROOT}/.venv/bin/activate"
fi

cd "${GIT_ROOT}"

echo $GIT_ROOT

python3 -m pip install -e .
python3 -m pip install --upgrade pip wheel build
python3 -m build .
# python3 -m setup.py sdist bdist_wheel

cd "${CURRENT_DIR}"

# exit venv if was not previously within one
if [ NOT_IN_VENV ]
then
    deactivate
fi