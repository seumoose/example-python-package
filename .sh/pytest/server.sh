#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
GIT_ROOT=$(git rev-parse --show-toplevel)
NOT_IN_VENV=`type deactivate &>/dev/null`

if [[ $# -ne 1 ]]
then
    echo "Port must be provided as the first parameter!"
    exit 1
else
    PORT=${1}
fi

# create virtual environment
$("${GIT_ROOT}/.sh/create_venv")

# acctivate virtual environment if not already in one
if [ NOT_IN_VENV ]
then
    source "${GIT_ROOT}/.venv/bin/activate"
fi

cd "${GIT_ROOT}"

# install dependancies
pip install -e .[dev]

cd "${GIT_ROOT}/reports/pytest/html"

python3 -m http.server ${PORT}

cd "${CURRENT_DIR}"

# exit venv if was not previously within one
if [ NOT_IN_VENV ]
then
    deactivate
fi