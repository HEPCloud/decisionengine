#!/bin/bash

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

DE_GIT_DEFAULT="https://github.com/HEPCloud/decisionengine.git"
DEM_GIT_DEFAULT="https://github.com/HEPCloud/decisionengine_modules.git"
DE_USER_DEFAULT=decisionengine

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
robust_realpath() {
    if ! realpath "$1" 2>/dev/null; then
        echo "$(cd "$(dirname "$1")"; pwd -P)/$(basename "$1")"
    fi
}

REQUIRED_RPM=decisionengine-modules-deps

# https://packaging.python.org/en/latest/specifications/version-specifiers/
help_msg() {
    cat << EOF
$0 [options]
Install the Decision Engine (Framework and Modules) Python release via pip. Requires the RPM installation.
--help                 Print this
--verbose              Verbose output
--de-repo-git URI      Decision Engine framework Git repository URI (default: $DE_GIT_DEFAULT)
--dem-repo-git URI     Decision Engine modules Git repository URI (default: $DEM_GIT_DEFAULT). Keywords:
                       same - relative to the framework repository
                       default - $DEM_GIT_DEFAULT
--de-git-ref REF       Decision Engine framework Git repository reference (default: "" - master). Keywords:
                       auto - Get the reference form the RPM installation version and release
                              Release is considered only for RCs (e.g. 2.0.4-N -> 2.0.4, 2.1.0-0.4.rc4 -> 2.1.0.rc4)
--dem-git-ref REF      Decision Engine modules Git repository reference (default: same as DE). Same keywords as --de-git-ref
--de-repo-dir PATH     Decision Engine framework Git repository directory
--dem-repo-dir PATH    Decision Engine modules Git repository directory (default: relative to DE directory)

--user USER            User to install and run Decision Engine (default: $DE_USER_DEFAULT)
--remote               Pip Installation from the DE and DEM Git (GitHub) URIs (default)
--local                Pip Installation from the local DE and DEM directory
--clone                Make a local clone of the repositories
Not yet implemented
--python PYTHON        Python interpreter or venv to use for Decision Engine
--dev                  Pip development Installation from the local DE and DEM directory
Examples:
To install the latest DE from GitHub ($DE_GIT_DEFAULT): $0
To install 2.1.0.rc2 from your GitHub repo: $0 --de-repo-git "https://github.com/YOUR_USER/decisionengine.git" --de-git-ref 2.1.0.rc2
EOF
}

parse_opts() {
    # Parse options. Uses SCRIPT_DIR
    # Sets VERBOSE, DO_CLONE, DE_GIT, REL_TAG, DE_DIR, DEM_GIT, DEM_DIR
    VERBOSE=false
    DE_USER="$DE_USER_DEFAULT"
    DE_PYTHON=python3
    DE_GIT="$DE_GIT_DEFAULT"
    DE_GIT_REF=
    DE_DIR=
    DEM_GIT=
    DEM_GIT_DEFAULT="https://github.com/HEPCloud/decisionengine_modules.git"
    DEM_GIT_REF=
    DEM_DIR=
    DO_CLONE=false
    INSTALL_TYPE="remote"
    while [ -n "$1" ];do
        case "$1" in
            --de-repo-git)
                DE_GIT="$2"
                shift
                ;;
            --de-git-ref)
                DE_GIT_REF="$2"
                shift
                ;;
            --de-repo-dir)
                DE_DIR="$2"
                shift
                ;;
            --dem-repo-git)
                if [[ "$2" = default ]];then
                    DEM_GIT="$DEM_GIT_DEFAULT"
                else
                    DEM_GIT="$2"
                fi
                shift
                ;;
            --dem-git-ref)
                DEM_GIT_REF="$2"
                shift
                ;;
            --dem-repo-dir)
                DEM_DIR="$2"
                shift
                ;;
            --user)
                DE_USER="$2"
                shift
                ;;
            --python)
                DE_PYTHON="$2"
                shift
                ;;
            --clone)
                DO_CLONE=true
                ;;
            --verbose)
                VERBOSE=true
                ;;
            --remote)
                INSTALL_TYPE="remote"
                ;;
            --local)
                INSTALL_TYPE="local"
                ;;
            --dev)
                INSTALL_TYPE="devel"
                ;;
            --help)
                help_msg
                exit 0
                ;;
            *)
                echo "Error. Parameter '$1' is not supported."
                help_msg
                exit 1
        esac
        shift
    done
    # Git URL and reference normalization
    if [[ -z  "$DEM_GIT" || "$DEM_GIT" = same ]]; then
        DEM_GIT="${DE_GIT%.git}_modules.git"
    fi
    [[ -n "$DE_GIT_REF" ]] && DE_GIT_REF="@$DE_GIT_REF" || true
    [[ -n "$DEM_GIT_REF" ]] && DEM_GIT_REF="@$DEM_GIT_REF" || DEM_GIT_REF="$DE_GIT_REF"
    # Checks for local directories
    if [[ "$INSTALL_TYPE" = local || "$INSTALL_TYPE" = devel ]] && ! $DO_CLONE; then
        # Must have local repositories
        [[ -n "$DE_DIR" && -d "$DE_DIR" ]] || { echo "Error. Local install without cloning and no valid DE repository ($DE_DIR). Aborting"; exit 1; }
        [[ -n "$DEM_DIR" ]] || DEM_DIR="$DE_DIR"/../decisionengine_modules
        [[ -d "$DEM_DIR" ]] || { echo "Error. Local install without cloning and no valid DEM repository ($DEM_DIR). Aborting"; exit 1; }
    fi
    # Relative DEM directory if not set and relative path to DE is there
    if [[ -n "$DE_DIR" && -z "$DEM_DIR" ]]; then
        [[ -d "$DE_DIR" && -d "$DE_DIR/../decisionengine_modules" ]] && DEM_DIR="$DE_DIR"/../decisionengine_modules || true
    fi
}

get_version() {
    local retv
    if ! retv=$(rpm -q "$REQUIRED_RPM"); then
        echo "Required RPMs ($REQUIRED_RPM) are not installed. Aborting"
	exit 1
    fi
    retv=${retv#${REQUIRED_RPM}-}
    $VERBOSE && echo "RPM Decision Engine version: $retv" || true
    echo ${retv%.*.noarch}
}

do_install_pre() {
    # Update pip
    pip install --upgrade pip
    # setuptools>71 incompatible w/ packaging <22, https://github.com/pypa/setuptools/issues/4483
    pip install --upgrade setuptools wheel setuptools-scm[toml] packaging
}

do_install() {
    retv=0
    # Install the Python modules via pip
    $VERBOSE && echo "Installing via pip git+$DE_FROM$DE_GIT_REF" || true
    pip install "git+$DE_FROM$DE_GIT_REF" || retv=1
    $VERBOSE && echo "Installing via pip git+$DEM_FROM$DEM_GIT_REF" || true
    pip install "git+$DEM_FROM$DEM_GIT_REF" || retv=1
    # Double check that pip added $HOME/.local/bin to the PATH of user decisionengine
    return $retv
}

do_install_su() {
    local cmd
    cmd="$(declare -f do_install_pre)
do_install_pre"
    # Update pip
    su -s /bin/bash -c "$cmd" -l "$DE_USER"
    # Install DE+DEM
    cmd="$(declare -f do_install)
DE_FROM='$DE_FROM'
DE_GIT_REF='$DE_GIT_REF'
DEM_FROM='$DEM_FROM'
DEM_GIT_REF='$DEM_GIT_REF'
do_install"
    su -s /bin/bash -c "$cmd" -l "$DE_USER"
}

make_dir() {
    local src_tmpdir=
    if [[ -z "$DE_DIR" || -z "$DEM_DIR" ]]; then
        # mktemp for both Linux and Darwin
        src_tmpdir=$(mktemp -d 2>/dev/null || mktemp -d -t 'detmpdir')
        [[ -n "$DE_DIR" ]] || DE_DIR="$src_tmpdir"/decisionengine
        [[ -n "$DEM_DIR" ]] || DEM_DIR="$src_tmpdir"/decisionengine_modules
    fi
}

clone_repo() {
    mkdir -p "$1"
    pushd "$1"
    git clone "$2" .
    [[ -n "$3" ]] && git checkout "${3#@}"
    popd
}

_main() {
    local de_rpm_version_release de_git_version
    # Check RPM requirements and get RPM version
    de_rpm_version_release=$(get_version)
    # Parse options and adjust parameters
    parse_opts "$@"
    # Deriving Git version
    if [[ "$de_rpm_version_release" = *rc* ]]; then
        # Extract the RPM release if RC (Python schema is X.Y.ZrcN, no dot)
        de_git_version="rc${de_rpm_version_release#*rc}"
    fi
    de_git_version="${de_rpm_version_release%-*}$de_git_version"
    [[ "$DE_GIT_REF" = "@auto" ]] && DE_GIT_REF="@$de_git_version" || true
    [[ "$DEM_GIT_REF" = "@auto" ]] && DEM_GIT_REF="@$de_git_version" || true
    $VERBOSE && echo "Corresponding Python version: $de_git_version ($DE_GIT_REF/$DEM_GIT_REF)"

    local src_tmpdir=
    if $DO_CLONE; then
        # Clone on disk
        if [[ -z "$DE_DIR" || -z "$DEM_DIR" ]]; then
            # mktemp for both Linux and Darwin
            src_tmpdir=$(mktemp -d 2>/dev/null || mktemp -d -t 'detmpdir')
            [[ -n "$DE_DIR" ]] || DE_DIR="$src_tmpdir"/decisionengine
            [[ -n "$DEM_DIR" ]] || DEM_DIR="$src_tmpdir"/decisionengine_modules
        fi
        clone_repo "$DE_DIR" "$DE_GIT" "$DE_GIT_REF"
	clone_repo "$DEM_DIR" "$DEM_GIT" "$DEM_GIT_REF"
    fi

    # Robust absolute path
    DE_DIR=$(robust_realpath "$DE_DIR")
    DEM_DIR=$(robust_realpath "$DEM_DIR")

    # Do install
    if [[ "$INSTALL_TYPE" = "local" ]]; then
        # This requires absolute paths
        DE_FROM="file://$DE_DIR"
        DEM_FROM="file://$DEM_DIR"
        $VERBOSE && echo "Preparing for local install from $DE_FROM, $DEM_FROM" || true
    elif [[ "$INSTALL_TYPE" = "remote" ]]; then
        DE_FROM="$DE_GIT"
        DEM_FROM="$DEM_GIT"
        $VERBOSE && echo "Preparing for remote install from $DE_FROM$DE_GIT_REF, $DEM_FROM$DEM_GIT_REF" || true
    else
        echo "Error: $INSTALL_TYPE not supported. Aborting"
	help_msg
        exit 1
    fi

    if [[ "$DE_USER" = $(whoami) ]]; then
        do_install_pre
        do_install
    else
        $VERBOSE && echo "Installing as user $DE_USER" || true
        do_install_su
    fi
    if [[ $? -ne 0 ]]; then
        echo "Error during the installation"
        exit 1
    else
        $VERBOSE && echo "Installation successful" || true
    fi

    # Clean temp dir if created
    if [[ -n "$src_tmpdir" ]]; then
        rm -rf "$src_tmpdir"
    fi
}

# https://stackoverflow.com/questions/29966449/what-is-the-bash-equivalent-to-pythons-if-name-main
# Alt: [[ "$(caller)" != "0 "* ]] || _main "$@"
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    _main "$@"
fi
