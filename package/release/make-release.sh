#!/bin/bash

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

#

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
robust_realpath() {
    if ! realpath "$1" 2>/dev/null; then
        echo "$(cd "$(dirname "$1")"; pwd -P)/$(basename "$1")"
    fi
}

# https://packaging.python.org/en/latest/specifications/version-specifiers/
help_msg() {
    cat << EOF
$0 [options] VERSION [RELEASE]
Build the Decision Engine (Framework and Modules) release (RPM for now, will build also PIP release).
VERSION RPM version string, e.g. 2.0.3
RELEASE RPM release string (default: 1), e.g. 1 or 0.1.rc1 or rc1 (equal to 0.1.rc1)
  -h       print this message
  -v       verbose mode
  -l       write RPM building logs in work directory
  -e       write RPM building logs to stderr
  -s TAG   source tag or reference to checkout when cloning the Git repository (default: current REF, or master for new clones)
           This is used only together with -c. It is ignored otherwise
           a - means that the tag is automatically evaluated from the RELEASE and VERSION
               for main releases it is the same as the version string
               for release candidates it is VERSIONrcN where N is the RC number
  -c URI   HTTPS URI of the decisionengine Git repository to clone to use to build the release
           The decisionengine_modules repository is derived replacing decisionengine.git with decisionengine_modules.git
  -p PLATFORM architecture or platform of the RPM package (default: alma+epel-9-x86_64)
              If you specify only an architecture (e.g. x86_64 or aarch64) alma+epel-9 is assumed
  -y PY_VER Python version e.g. 311 or python311 (default: python39)
  -r DE_DIR directory of the decisionengine Git repository (default: ../../ from this script)
  -m DEM_DIR directory of the decisionengine_modules Git repository (default: ../../../decisionengine_modules from this script)
  -d REL_DIR directory where to build the release (default: $PWD)
  -w YUM_REPO publish the RPMs to the YUM repository in YUM_REPO
EOF
}

parse_opts() {
    # Parse options. Uses SCRIPT_DIR
    # Sets VERBOSE, DO_CLONE, REL_DIR, REL_TAG, DE_DIR, DEM_DIR
    VERBOSE=
    CLONE_URI=
    CMD_LOGS="/dev/null"
    REL_DIR="$PWD"
    SRC_TAG=
    DE_DIR=
    DEM_DIR=
    RPM_PLATFORM="alma+epel-9-x86_64"
    PY_VER=python39
    YUM_REPO=
    while getopts "vlecs:p:y:r:m:d:w:h" option
    do
      case "${option}"
        in
        h) help_msg; exit 0;;
        v) VERBOSE=yes;;
        l) CMD_LOGS="de";;
        e) CMD_LOGS="/dev/stderr";;
        c) CLONE_URI="$OPTARG";;
        s) SRC_TAG="$OPTARG";;
        p) RPM_PLATFORM="$OPTARG";;
        y) PY_VER="$OPTARG";;
        r) DE_DIR="${OPTARG%/}";;
        m) DEM_DIR="${OPTARG%/}";;
        d) REL_DIR="${OPTARG%/}";;
        w) YUM_REPO="${OPTARG%/}";;
        *) echo "ERROR: Invalid option"; help_msg; exit 1;;
      esac
    done
    # If there is no dash assume it is only the architecture
    [[ "$RPM_PLATFORM" = *-* ]] || RPM_PLATFORM="alma+epel-9-$RPM_PLATFORM"
    PY_VER=python${PY_VER#python}
    if [[ -z "$CLONE_URI" ]]; then
        [[ -n "$DE_DIR" ]] || DE_DIR="$SCRIPT_DIR"/../..
        [[ -n "$DEM_DIR" ]] || DEM_DIR="$DE_DIR"/../decisionengine_modules
    fi
}

prepare_rpmmacros() {
    # Write rpmmacros file. Uses RPM_ROOT_DIR
    cat << EOF > "$REL_DIR"/rpmmacros
_topdir $RPM_ROOT_DIR
_tmppath /tmp
_source_filedigest_algorithm md5
_binary_filedigest_algorithm md5
EOF
}

get_rc_number() {
    # Return the RC number, empty for main releases
    # 1 - release string
    [[ "$1" = *rc* ]] && echo "${1#*rc}"
}

get_srpm_file() {
    # Guess the SRPM file in case of OS changes. File name is like name-${VERSION}-${RELEASE}.${OS}.src.rpm
    # Get the name is OS is different from the expected one (el9)
    # 1 - Expected path of the SRPM file with the expected OS
    local retv
    local prefix="${1%.src.rpm}"
    retv=$(ls "${prefix%.*}".* 2>/dev/null)
    [[ -n "$retv" ]] && echo "${retv}" || echo "$1"
}

clone_repositories() {
    # Clone Git repositories. Uses VERBOSE, DE_DIR, DEM_DIR
    # 1 - decisionengine Git repository HTTPS URI
    # 2 (optional) - Git reference to checkout
    local ec=0
    [[ -n "$VERBOSE" ]] && echo "Cloning the DE and DEM repositories from: $1" && echo "to: $DE_DIR, $DEM_DIR" || true
    mkdir -p "$DE_DIR" && pushd "$DE_DIR" 2> /dev/null
    git clone "$1" . || ec=1
    [[ -z "$2" ]] || git checkout "$2"
    popd 2> /dev/null
    mkdir -p "$DEM_DIR" && pushd "$DEM_DIR" 2> /dev/null
    git clone "${1%decisionengine.git}decisionengine_modules.git" . || ec=1
    [[ -z "$2" ]] || git checkout "$2"
    popd 2> /dev/null
    return $ec
}

release_rpm() {
    # Make the RPM release.
    # Uses DE_VERSION, DE_RELEASE, RPM_ROOT_DIR, REL_DIR, CMD_LOGS, VERBOSE, RPM_PLATFORM, PY_VER, YUM_REPO
    # Prepare spec file
    sed -e "s/__HCDE_RPM_VERSION__/${DE_VERSION}/" -e "s/__HCDE_RPM_RELEASE__/${DE_RELEASE}/" "$DE_DIR"/package/rpm/decisionengine.spec > "$RPM_ROOT_DIR"/SPECS/decisionengine.spec
    # Copy sources
    # The empty tar file is a placeholder
    rm -rf "$REL_DIR"/tmp
    mkdir -p "$REL_DIR"/tmp/hepcloud && pushd "$REL_DIR"/tmp 2> /dev/null && \
        tar czf "$RPM_ROOT_DIR"/SOURCES/hepcloud.tar.gz hepcloud && popd 2> /dev/null || \
        { echo "Failed to create empty source. Aborting."; exit 1; }
    cp "$DE_DIR"/config/decision_engine.jsonnet "$RPM_ROOT_DIR"/SOURCES/
    # Build SRPM
    [[ -n "$VERBOSE" ]] && echo "Building the source RPM for $DE_VERSION-$DE_RELEASE" || true
    [[ "$CMD_LOGS" = /dev/* ]] || CMD_LOGS="${CMD_LOGS}.srpm.log"
    eval "rpmbuild -bs \"$RPM_ROOT_DIR/SPECS/decisionengine.spec\" $(while IFS= read -r i ; do echo -n "--define \"$i\" "; done < "$REL_DIR"/rpmmacros;)" 2>"$CMD_LOGS"
    srpm_file=$(get_srpm_file "$RPM_ROOT_DIR/SRPMS/decisionengine-${DE_VERSION}-${DE_RELEASE}.el9.src.rpm")
    [[ -f "$srpm_file" ]] || { echo "SRPM build failed ($srpm_file). Aborting."; exit 2; }
    [[ -n "$VERBOSE" ]] && echo "Building the RPM for $RPM_PLATFORM via mock" || true
    [[ "$CMD_LOGS" = /dev/* ]] || CMD_LOGS="${CMD_LOGS%.srpm.log}.mockenv.log"
    if ! mock -r "$RPM_PLATFORM" --macro-file="$REL_DIR"/rpmmacros -i "$PY_VER" 2>"$CMD_LOGS"; then
        echo "Error setting up the mock environment. Aborting"
        exit 2
    fi
    [[ "$CMD_LOGS" = /dev/* ]] || CMD_LOGS="${CMD_LOGS%.mockenv.log}.mockrpm.log"
    if ! mock --no-clean -r "$RPM_PLATFORM" --macro-file="$REL_DIR"/rpmmacros --resultdir="$RPM_ROOT_DIR"/RPMS rebuild "$srpm_file" 2>"$CMD_LOGS"; then
        echo "Error building the RPM via mock. Aborting"
        exit 2
    fi
    [[ -n "$VERBOSE" ]] && echo "RPMs are in $RPM_ROOT_DIR/RPMS" || true
    # Update the YUM repository
    if [[ -n "$YUM_REPO" ]];then
        [[ -n "$VERBOSE" ]] && echo "Deploying RPMs in YUM repository: $YUM_REPO" || true
        cp "$RPM_ROOT_DIR/RPMS/decisionengine-${DE_VERSION}-${DE_RELEASE}.*rpm" "$YUM_REPO"/
        if ! createrepo "$YUM_REPO"; then
            echo "Error updating the YUM repository. Aborting"
            exit 2
        fi
    fi
}

_main() {
    # Parse options and adjust parameters
    parse_opts "$@"
    # This needs to be outside to shift the general arglist
    shift $((OPTIND-1))
    DE_VERSION=$1
    [[ -n "$DE_VERSION" ]] || { echo "Error: you must specify the RELEASE."; help_msg; exit 1; }
    DE_RELEASE=${2:-1}
    DE_RELEASE=${DE_RELEASE,,}
    [[ "$DE_RELEASE" = rc* ]] && DE_RELEASE="0.${DE_RELEASE#rc}.$DE_RELEASE"
    [[ "$SRC_TAG" = a ]] && SRC_TAG="$DE_VERSION$(get_rc_number "$DE_RELEASE")" || true
    REL_DIR=$(robust_realpath "$REL_DIR")
    RPM_ROOT_DIR="$REL_DIR"/rpmbuild
    if [[ "$CMD_LOGS" = de ]]; then
        CMD_LOGS="$REL_DIR/${CMD_LOGS}-${DE_VERSION}-${DE_RELEASE}"
        [[ -n "$VERBOSE" ]] && echo "Log files will be in $REL_DIR/${CMD_LOGS}-${DE_VERSION}-${DE_RELEASE}\*"
    fi
    local src_tmpdir=
    if [[ -z "$DE_DIR" || -z "$DEM_DIR" ]]; then
        # mktemp for both Linux and Darwin
        src_tmpdir=$(mktemp -d 2>/dev/null || mktemp -d -t 'detmpdir')
        [[ -n "$DE_DIR" ]] || DE_DIR="$src_tmpdir"/decisionengine
        [[ -n "$DEM_DIR" ]] || DEM_DIR="$src_tmpdir"/decisionengine_modules
    fi
    DE_DIR=$(robust_realpath "$DE_DIR")
    DEM_DIR=$(robust_realpath "$DEM_DIR")

    # Start setup
    [[ -n "$VERBOSE" ]] && echo "Setting up release work directory: $REL_DIR" || true
    mkdir -p "$RPM_ROOT_DIR"
    prepare_rpmmacros
    for i in BUILD  BUILDROOT  RPMS	SOURCES  SPECS	SRPMS; do
        mkdir -p "$RPM_ROOT_DIR"/$i
    done
    # Cloning repos
    if [[ -n "$CLONE_URI" ]]; then
        if ! clone_repositories "$CLONE_URI" "$SRC_TAG"; then
            echo "Error cloning the Git repositories as requested. Aborting"
            exit 2
        fi
    fi

    # Make the RPM release
    release_rpm

    # Removing temp dir if any
    [[ -z "$src_tmpdir" ]] || rm -rf "$src_tmpdir"
}

# https://stackoverflow.com/questions/29966449/what-is-the-bash-equivalent-to-pythons-if-name-main
# Alt: [[ "$(caller)" != "0 "* ]] || _main "$@"
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    _main "$@"
fi
