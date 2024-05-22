#!/usr/bin/env bash

# Usage: /path/to/this/file/scan http://some.sonarqube.domain:1234 what-your-login-token-is

# Note: not currently working
# TODO: get sonarqube scanning working and figure out what needs to be changed

SONARQUBE_HOST="$1"
SONARQUBE_TOKEN="$2"
GIT_ROOT=$(git rev-parse --show-toplevel)

docker pull sonarsource/sonar-scanner-cli

docker run \
    --rm \
    --net=host \
    -e SONAR_HOST_URL="${SONARQUBE_HOST}" \
    -e SONAR_LOGIN="${SONARQUBE_TOKEN}" \
    -v "${GIT_ROOT}:/usr/dir" \
    sonarsource/sonar-scanner-cli \
    -Dproject.settings="/usr/dir/sonar-project.properties"