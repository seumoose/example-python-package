#!/usr/bin/env bash

GIT_ROOT=$(git rev-parse --show-toplevel)

# create a .venv directory if one doesn't already exist
if [ ! -d "${GIT_ROOT}/.venv" ]
then
    python3 -m venv "${GIT_ROOT}/.venv"
fi