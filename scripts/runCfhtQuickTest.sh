#!/bin/bash

set -e

PRODUCT_DIR=${LSST_CI_DIR}
if [[ ${PRODUCT_DIR} == '' ]]; then
    PRODUCT_DIR='.'
fi
VALIDATION_DATA_DIR="$VALIDATION_DATA_CFHT_DIR/raw"
PHOTOMETRIC_REF_CAT_DIR="$VALIDATION_DATA_CFHT_DIR/ref_cats"

CAMERA=CfhtQuick
CONFIG_FILE="${PRODUCT_DIR}/config/cfhtConfig.py"
MAPPER=lsst.obs.cfht.MegacamMapper

print_error() {
    >&2 echo "$@"
}

DOPROCESS=true
DOVERIFY=true

usage() {
    print_error
    print_error "Usage: $0 [-PV] [-h] [-- <extra options to validateDrp.py>]"
    print_error
    print_error "Specifc options:"
    print_error "   -P          Skip processing?"
    print_error "   -V          Skip verification?"
    print_error "   -h          show this message"
    exit 1
}

while getopts "VP" option; do
    case "$option" in
        P)  DOPROCESS=false;;
        V)  DOVERIFY=false;;
        h)  usage;;
        *)  usage;;
    esac
done
shift $((OPTIND-1))

if [[ $DOPROCESS == true ]]; then
    "${PRODUCT_DIR}/scripts/processData.sh" \
        -c "$CAMERA" \
        -m "$MAPPER" \
        -v "$VALIDATION_DATA_DIR" \
        -p "$PHOTOMETRIC_REF_CAT_DIR" \
        -f "$CONFIG_FILE"
fi

if [[ $DOVERIFY == true ]]; then
    "${PRODUCT_DIR}/scripts/validateRepo.sh" \
        -c "$CAMERA" \
        -- "$@"
fi
