#!/bin/bash

set -e

print_error() {
    >&2 echo "$@"
}

usage() {
    print_error
    print_error "Usage: $0 [-cmvfip] [-h] [-- <options to validateDrp.py>]"
    print_error
    print_error "Specifc options:"
    print_error "   -c          camera"
    print_error "   -h          show this message"
    exit 1
}

while getopts "c:h" option; do
    case "$option" in
        c)  CAMERA="$OPTARG";;
        h)  usage;;
        *)  usage;;
    esac
done
shift $((OPTIND-1))

PRODUCT_DIR=${VALIDATE_DRP_DIR}
# OS X El Capitan SIP swallows DYLD_LIBRARY_PATH so export the duplicate in LSST_LIBRARY_PATH
if [[ -z $DYLD_LIBRARY_PATH ]]; then
    export DYLD_LIBRARY_PATH=$LSST_LIBRARY_PATH
fi

WORKSPACE=${CAMERA}

OUTPUT=${WORKSPACE}/output

if ! [[ -d $OUTPUT ]]; then
    print_error "Repository does not exist.  Please run processData.sh first."
    exit 1
fi

# YAML config file for validation configuration
YAMLCONFIG="${PRODUCT_DIR}"/scripts/${CAMERA}.yaml

# Run astrometry check on src
echo "validating"
validateDrp.py "${OUTPUT}" --configFile "${YAMLCONFIG}" "$@"
