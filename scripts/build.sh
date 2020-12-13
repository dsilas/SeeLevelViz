#!/usr/bin/env bash
# USAGE: bash scripts/build.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${SCRIPT_DIR}/.."

for i in "$@"
do
case $i in
    --help*)
    echo "USAGE: bash scripts/build.sh"
    exit
    shift
    ;;
    *)
    # unknown option
    ;;
esac
done

docker build -t seelevelviz .