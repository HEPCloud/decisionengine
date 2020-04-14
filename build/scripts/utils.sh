#!/bin/sh

log_nonzero_rc() {
    echo "`date` ERROR: $1 failed with non zero exit code ($2)" 1>&2
}


setup_python_venv() {
    if [ $# -gt 2 ]; then
        echo "Invalid number of arguments to setup_python_venv. Will accept the location to install venv or use PWD as default"
        exit 1
    fi
    WORKSPACE=${1:-`pwd`}
    PYVER=${2:-"3.6"}
    VENV=$WORKSPACE/venv-$PYVER

    # Following is useful for running the script outside jenkins
    #if [ ! -d "$WORKSPACE" ]; then
    #    mkdir $WORKSPACE
    #fi

    VIRTUALENV_EXE=virtualenv
    PIP_EXE=pip

    if [ "$PYVER" == "3.6" ]; then
      VIRTUALENV_EXE=virtualenv-3.6
    fi

    if [ ! -d $VENV ] ; then
         if [ "$PYVER" == "3.6" ]; then
             $VIRTUALENV_EXE $VENV
         else
             $VIRTUALENV_EXE --system-site-packages $VENV
         fi
    fi

    source $VENV/bin/activate
    export PYTHONPATH="$PWD:$PYTHONPATH"

    # Install dependancies first so we don't get uncompatible ones
    # Following RPMs need to be installed on the machine:
    #pip_packages="astroid pylint pep8 unittest2 coverage sphinx DBUtils pytest"
    pip_packages="argparse WebOb astroid pylint pycodestyle unittest2 coverage sphinx tabulate DBUtils psycopg2 pytest mock pandas ipython"
    for package in $pip_packages; do
        echo "Installing $package ..."
        status="DONE"
        pip install --quiet $package
        if [ $? -ne 0 ]; then
            status="FAILED"
        fi
        echo "Installing $package ... $status"
    done

    # Need this because some strange control sequences when using default TERM=xterm
    export TERM="linux"

    # PYTHONPATH for decision engine source code
    export PYTHONPATH=${PYTHONPATH}:${DECISIONENGINE_SRC}
}


setup_glideinwms() {
    WSPACE=${1:-`pwd`}
    glideinwms_git="https://github.com/glideinWMS/glideinwms.git"
    cd $WSPACE
    git clone $glideinwms_git
}

setup_dependencies() {
    WORKSPACE=${1:-`pwd`}
    DEPS_DIR=$WORKSPACE/dependencies
    rm -rf $DEPS_DIR
    mkdir $DEPS_DIR
    touch $DEPS_DIR/__init__.py

    setup_glideinwms $DEPS_DIR
    export PYTHONPATH=$DEPS_DIR
    cd $WORKSPACE
}


print_python_info() {
    if [ $# -ne 0 ]; then
        br="<br/>"
        bo="<b>"
        bc="</b>"
    fi
    echo "${bo}HOSTNAME:${bc} `hostname -f`$br"
    echo "${bo}LINUX DISTRO:${bc} `lsb_release -d`$br"
    echo "${bo}PYTHON:${bc} `which python`$br"
    echo "${bo}PYLINT:${bc} `pylint --version`$br"
    echo "${bo}PEP8:${bc} `pycodestyle --version`$br"
}


mail_results() {
    local contents=$1
    local subject=$2
    local to=$3
    local attachments=$4
    local from="parag@fnal.gov"
#    echo "From: parag@fnal.gov;
#To: parag@fnal.gov;
#Subject: $subject;
#Content-Type: text/html;
#MIME-VERSION: 1.0;
#;
#`cat $contents`
#" | sendmail -t
    local attach=""
    [ -n "$attachments" ] && attach=" -a `echo $attachments | sed -e 's|,| -a |g'`"
    mutt -e "set content_type=text/html"  -s "$subject" $to $attach < $contents
}
