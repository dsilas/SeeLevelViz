#!/usr/bin/env bash
# USAGE: bash scripts/run.sh --dem_file=data/elecation_rez50.tif --input=input.csv

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${SCRIPT_DIR}/.."

for i in "$@"
do
case $i in
    --dem_file=*)
    DEM_FILE="${i#*=}"
    shift # past argument=value
    ;;
    --input=*)
    INPUT_FILE="${i#*=}"
    shift # past argument=value
    ;;
    --help*)
    echo "USAGE: bash scripts/run.sh --dem_file=data/elecation_rez50.tif --input=input.csv"
    exit
    shift
    ;;
    *)
    # unknown option
    ;;
esac
done

# require dem_file
if [ -z "$DEM_FILE" ]
then
    echo "--dem_file is required"
    exit
fi

# require dem_file
if [ -z "$INPUT_FILE" ]
then
    echo "--input is required"
    exit
fi

docker build -t seelevelviz:latest --dem_file="${DEM_FILE}" --input="${INPUT_FILE}"

set +e