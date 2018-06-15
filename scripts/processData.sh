#!/bin/bash

set -e

print_error() {
    >&2 echo "$@"
}

INGEST=ingestImages.py
INGESTEXT=fz
ASTROMDIR=astrometry_net_data

usage() {
    print_error
    print_error "Usage: $0 [-cmvfioear] [-h]"
    print_error
    print_error "Specifc options:"
    print_error "   -c          Camera"
    print_error "   -m          Mapper"
    print_error "   -v          Validation data"
    print_error "   -f          Config file"
    print_error "   -i          Ingest script"
    print_error "   -o          Extra options for ingest script"
    print_error "   -e          Extension to ingest"
    print_error "   -a          Name of astrometry to load"
    print_error "   -r          Reduce from raw?  Implies there is a CALIB directory"
    print_error "   -d          Path to calibs"
    print_error "   -h          show this message"
    exit 1
}

while getopts "c:m:v:f:i:o:e:a:d:hr" option; do
    case "$option" in
        c)  CAMERA="$OPTARG";;
        m)  MAPPER="$OPTARG";;
        v)  VALIDATION_DATA="$OPTARG";;
        f)  CONFIG_FILE="$OPTARG";;
        i)  INGEST="$OPTARG";;
        o)  INGESTARGS="$OPTARG";;
        e)  INGESTEXT="$OPTARG";;
        a)  ASTROMDIR="$OPTARG";;
        r)  DOCALIB=true;;
        d)  CALIB_DATA="$OPTARG";;
        h)  usage;;
        *)  usage;;
    esac
done
shift $((OPTIND-1))

PRODUCT_DIR=${LSST_CI_DIR}
if [[ ${PRODUCT_DIR} == '' ]]; then
    PRODUCT_DIR='.'
fi
# OS X El Capitan SIP swallows DYLD_LIBRARY_PATH so export the duplicate in LSST_LIBRARY_PATH
if [[ -z $DYLD_LIBRARY_PATH ]]; then
    export DYLD_LIBRARY_PATH=$LSST_LIBRARY_PATH
fi

WORKSPACE=${CAMERA}
if [[ -d $WORKSPACE ]]; then
   rm -rf "${WORKSPACE}"
fi

# cleanup and create directories
echo "Ingesting Raw data"
INPUT=${WORKSPACE}/input
mkdir -p "$INPUT"
OUTPUT=${WORKSPACE}/output
mkdir -p "$OUTPUT"

echo "$MAPPER" > "${INPUT}"/_mapper

# ingest raw data
RAWDATA=${VALIDATION_DATA}
$INGEST "${INPUT}" "${RAWDATA}"/*."${INGESTEXT}" --mode link ${INGESTARGS}

# set up calibs
if [[ $DOCALIB == true ]]; then
    ln -s "${CALIB_DATA}" "${WORKSPACE}"/CALIB
fi

# Set up astrometry
export SETUP_ASTROMETRY_NET_DATA="astrometry_net_data ${ASTROMDIR}"
export ASTROMETRY_NET_DATA_DIR="${VALIDATION_DATA}"/../"${ASTROMDIR}"

# Create calexps and src
echo "running singleFrameDriver"
MACH=$(uname -s)
if [[ $MACH == Darwin ]]; then
    sys_proc=$(sysctl -n hw.logicalcpu)
else
    sys_proc=$(grep -c processor /proc/cpuinfo)
fi
max_proc=8
NUMPROC=${NUMPROC:-$((sys_proc < max_proc ? sys_proc : max_proc))}

# Extract desired dataIds runs from YAML config file
YAMLCONFIG="${PRODUCT_DIR}"/scripts/${CAMERA}.yaml
RUNLIST="${WORKSPACE}"/"${CAMERA}".list
makeRunList.py "${YAMLCONFIG}" > "${RUNLIST}"

CALIBSTRING=
if [[ $DOCALIB == true ]]; then
    CALIBSTRING="--calib $WORKSPACE/CALIB"
fi

# shellcheck disable=SC2086
singleFrameDriver.py "${INPUT}" $CALIBSTRING --output "${OUTPUT}" \
    @"${RUNLIST}" \
    -C "${CONFIG_FILE}" \
    --job validate_drp \
    --cores "$NUMPROC" \
    >& "${WORKSPACE}"/singleFrame.log
