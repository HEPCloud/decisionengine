#!/bin/sh

get_current_git_branch() {
    cd $DECISIONENGINE_SRC
    gb=`git branch | grep "\*" | cut -d ' ' -f2`
    cd $WORKSPACE
    echo $gb
}

process_branch() {
    local pylint_log=$1
    local pep8_log=$2
    local results=$3
    local git_branch=$4

    echo "===================================================================="
    echo "GIT BRANCH: $git_branch"
    echo "===================================================================="
    # Initialize logs
    > $pylint_log
    > $pep8_log
    > $results

    echo "GIT_BRANCH=\"$git_branch\"" >> $results
    if [ -n "$git_branch" ]; then
        cd $DECISIONENGINE_SRC
        git checkout $git_branch
        checkout_rc=$?
        #git pull
        cd $WORKSPACE
        if [ $checkout_rc -ne 0 ]; then
            log_nonzero_rc "git checkout" $?
            echo "GIT_CHECKOUT=\"FAILED\"" >> $results
            # HACK
            #return
        fi
    fi
    # Consider success if no git checkout was done
    echo "GIT_CHECKOUT=\"PASSED\"" >> $results

    # Build Logic Engine
    echo "Building Logic Engine ..."
    le_builddir=$DECISIONENGINE_SRC/framework/logicengine/cxx/build
    mkdir $le_builddir
    cd $le_builddir
    cmake --debug-output ..
    make --debug
    [ -e ../../RE.so ] && rm ../../RE.so
    [ -e ../../libLogicEngine.so ] && ../../libLogicEngine.so
    cp ErrorHandler/RE.so ../..
    cp ErrorHandler/libLogicEngine.so ../..
    echo "Building Logic Engine ... DONE"

    cd $WORKSPACE

    # pylint related variables
    PYLINT_RCFILE=/dev/null
    #PYLINT_RCFILE=$WORKSPACE/pylint.cfg
    #PYLINT_OPTIONS="--errors-only --msg-template=\"{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}\" --rcfile=$PYLINT_RCFILE"
    PYLINT_OPTIONS="--contextmanager-decorators=contextlib.contextmanager,tf_contextlib.contextmanager --errors-only --rcfile=$PYLINT_RCFILE --disable=no-member"

    # pep8 related variables
    # default: E121,E123,E126,E226,E24,E704
    # E501 line too long (90 > 79 characters)
    # E251 unexpected spaces around keyword / parameter equals
    # E303 too many blank lines (2)
    # E225 missing whitespace around operator
    # E231 missing whitespace after ','
    # E228 missing whitespace around modulo operator
    # E302 expected 2 blank lines, found 1
    # E221 multiple spaces before operator
    # E261 at least two spaces before inline comment
    # E111 indentation is not a multiple of four
    # W293 blank line contains whitespace
    # W291 trailing whitespace
    # E265 block comment should start with '# '

    PEP8_OPTIONS="--ignore=E121,E123,E126,E226,E24,E704,E501,E251,E303,E225,E231,E228,E302,E221,E261,E111,W293,W291,E265"

    # Generate pylint config file
    #pylint --generate-rcfile > $PYLINT_RCFILE
    #cat $PYLINT_RCFILE

    # get list of python scripts without .py extension
    #scripts=`find $DECISIONENGINE_SRC/framework $DECISIONENGINE_SRC/modules $DECISIONENGINE_SRC/util -name "*.py"`
    scripts=`find $DECISIONENGINE_SRC/framework $DECISIONENGINE_SRC/util -name "*.py"`
    currdir=`pwd`
    files_checked=""
    for file in $scripts
    do
        files_checked="$files_checked $file"
        pylint $PYLINT_OPTIONS $file >> $pylint_log || log_nonzero_rc "pylint" $?
        pycodestyle $PEP8_OPTIONS $file >> $pep8_log || log_nonzero_rc "pep8" $?
    done
    echo "FILES_CHECKED=\"$files_checked\"" >> $results
    echo "FILES_CHECKED_COUNT=`echo $files_checked | wc -w | tr -d " "`" >> $results
    echo "PYLINT_ERROR_FILES_COUNT=`grep '^\*\*\*\*\*\*' $pylint_log | wc -l | tr -d " "`" >> $results
    echo "PYLINT_ERROR_COUNT=`grep '^E:' $pylint_log | wc -l | tr -d " "`" >> $results
    echo "PEP8_ERROR_COUNT=`cat $pep8_log | wc -l | tr -d " "`" >> $results
    echo "----------------"
    cat $results
    echo "----------------"
}


init_results_mail () {
    local mail_file=$1
    echo -n > $mail_file
}

init_results_logging() {
    local mail_file=$1
    cat >> $mail_file << TABLE_START
<body>

  <p>
`print_python_info $mail_file`
  </p>
<table style="$HTML_TABLE">
  <thead style="$HTML_THEAD">
    <tr style="$HTML_TR">
      <th style="$HTML_THEAD_TH">GIT BRANCH</th>
      <th style="$HTML_THEAD_TH">FILES CHECKED</th>
      <th style="$HTML_THEAD_TH">FILES WITH ERRORS</th>
      <th style="$HTML_THEAD_TH">TOTAL ERRORS</th>
      <th style="$HTML_THEAD_TH">PEP8 ERRORS</th>
    </tr>
  </thead>
  <tbody>
TABLE_START

}


log_branch_results() {
    local mail_file=$1
    local branch_results=$2
    unset GIT_BRANCH
    unset GIT_CHECKOUT
    unset FILES_CHECKED_COUNT
    unset PYLINT_ERROR_FILES_COUNT
    unset PYLINT_ERROR_COUNT
    unset PEP8_ERROR_COUNT
    source $branch_results

    class=$GIT_CHECKOUT
    if [ "$class" = "PASSED" ]; then
        [ ${PYLINT_ERROR_COUNT:-1} -gt 0 ] && class="FAILED"
    fi
    if [ "$class" = "PASSED" ]; then
        cat >> $mail_file << TABLE_ROW_PASSED
<tr style="$HTML_TR">
    <th style="$HTML_TH">$GIT_BRANCH</th>
    <td style="$HTML_TD_PASSED">${FILES_CHECKED_COUNT:-NA}</td>
    <td style="$HTML_TD_PASSED">${PYLINT_ERROR_FILES_COUNT:-NA}</td>
    <td style="$HTML_TD_PASSED">${PYLINT_ERROR_COUNT:-NA}</td>
    <td style="$HTML_TD_PASSED">${PEP8_ERROR_COUNT:-NA}</td>
</tr>
TABLE_ROW_PASSED
    else
        cat >> $mail_file << TABLE_ROW_FAILED
<tr style="$HTML_TR">
    <th style="$HTML_TH">$GIT_BRANCH</th>
    <td style="$HTML_TD_FAILED">${FILES_CHECKED_COUNT:-NA}</td>
    <td style="$HTML_TD_FAILED">${PYLINT_ERROR_FILES_COUNT:-NA}</td>
    <td style="$HTML_TD_FAILED">${PYLINT_ERROR_COUNT:-NA}</td>
    <td style="$HTML_TD_FAILED">${PEP8_ERROR_COUNT:-NA}</td>
</tr>
TABLE_ROW_FAILED
    fi
}


finalize_results_logging() {
    local mail_file=$1
    cat >> $mail_file << TABLE_END
    </tbody>
</table>
</body>
TABLE_END
}

###############################################################################
# HTML inline CSS
HTML_TABLE="border: 1px solid black;border-collapse: collapse;"
HTML_THEAD="font-weight: bold;border: 0px solid black;background-color: #ffcc00;"
HTML_THEAD_TH="border: 0px solid black;border-collapse: collapse;font-weight: bold;background-color: #ffb300;padding: 8px;"

HTML_TH="border: 0px solid black;border-collapse: collapse;font-weight: bold;background-color: #00ccff;padding: 8px;"
HTML_TR="padding: 5px;text-align: center;"
HTML_TD="border: 1px solid black;border-collapse: collapse;padding: 5px;text-align: center;"

HTML_TR_PASSED="padding: 5px;text-align: center;"
HTML_TD_PASSED="border: 0px solid black;border-collapse: collapse;background-color: #00ff00;padding: 5px;text-align: center;"

HTML_TR_FAILED="padding: 5px;text-align: center;"
HTML_TD_FAILED="border: 0px solid black;border-collapse: collapse;background-color: #ff0000;padding: 5px;text-align: center;"



###############################################################################
# MAIN
###############################################################################

function usage {
    echo "Usage: run_pylint.sh <OPTIONS>"
    echo "OPTIONS:"
    echo "  -tags <git tags>           : List of comma separated tags/branches"
    echo "  -email <email address>     : Send results to the given email"

}

while [ $# -gt 0 ]
do case "$1" in
    -tags) git_branches="$2";;
    -email) email_to="$2";;
    *)  (warn "Unknown option $1"; usage) 1>&2; exit 1
esac
shift
shift
done


#git_branches="$1"
WORKSPACE=`pwd`
export DECISIONENGINE_SRC=$WORKSPACE/decisionengine

source $DECISIONENGINE_SRC/build/scripts/utils.sh
setup_python_venv $WORKSPACE

setup_dependencies $WORKSPACE
# Jenkins will reuse the workspace on the slave node if it is available
# There is no reason for not using it, but we need to make sure we keep
# logs for same build together to make it easier to attach to the email
# notifications or for violations. $BUILD_NUMBER is only available when
# running this script from the jenkins environment
LOG_DIR=$WORKSPACE/$BUILD_NUMBER
[ -d $LOG_DIR ] || mkdir -p $LOG_DIR

PYLINT_LOG=$LOG_DIR/pylint
PEP8_LOG=$LOG_DIR/pep8
RESULTS=$LOG_DIR/results
RESULTS_MAIL=$LOG_DIR/mail.results
LOG_EXT="log"
attachments=""

init_results_mail $RESULTS_MAIL
init_results_logging $RESULTS_MAIL

[ -z $git_branches ] && git_branches=`get_current_git_branch`

for gb in `echo $git_branches | sed -e 's/,/ /g'`
do
    if [ -n "$gb" ]; then
        gb_escape=`echo $gb | sed -e 's|/|_|g'`
        pylint_log="$PYLINT_LOG.$gb_escape.$LOG_EXT"
        pep8_log="$PEP8_LOG.$gb_escape.$LOG_EXT"
        results="$RESULTS.$gb_escape.$LOG_EXT"
    fi
    process_branch $pylint_log $pep8_log $results $gb
    log_branch_results $RESULTS_MAIL $results
    for log in $pep8_log $pylint_log ; do
        if [ -s $log ]; then
            if [ -z "$attachments" ]; then
                attachments=$log
            else
                attachments="$attachments,$log"
            fi
        fi
    done
done

finalize_results_logging $RESULTS_MAIL

echo "RESULTS can be found in $attachments in dir $WORKSPACE"
if [ -n "$email_to" ]; then
    echo "Mailing results to $email_to ..."
    mail_results $RESULTS_MAIL "Pylint/PEP8 Validation Results" "$email_to" $attachments
    echo "Mailing results to $email_to ... DONE"
else
    echo "Email not provided. Results will not be emailed."
fi
