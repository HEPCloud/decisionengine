#!/bin/bash

id=`whoami`
product=decisionengine

echo $#

if [ $# -eq 0 ] ; then
    source_dir=/cloud/login/parag/wspace/de/decisionengine
else
    source_dir=$1
fi

echo "Using source dir: $source_dir"
echo "Using Python version: $PYVER"

export RPM_TOPDIR=/var/tmp/$id/rpm/decisionengine
mkdir -p $RPM_TOPDIR

rpm_macros=~/.rpmmacros

cat > $rpm_macros << RPM_MACROS
%_topdir    %(echo \$RPM_TOPDIR)
%_builddir  %{_topdir}/BUILD
%_sourcedir %{_topdir}/SOURCES
%_rpmdir    %{_topdir}/RPMS
%_specdir   %{_topdir}/SPECS
%_srcrpmdir %{_topdir}/SRPMS
%_tmppath   %{_topdir}/TMP
%pyver %(echo \$PYVER)
RPM_MACROS

release_dir=/var/tmp/$id/release
product_release_dir=$release_dir/$product
release_tar=$release_dir/decisionengine.tar.gz

spec_template=$source_dir/build/packaging/rpm/decisionengine.spec
if [[ "$PYVER" == "3.6" ]];then
spec_template=$source_dir/build/packaging/rpm/decisionengine.spec
fi
spec_file=$RPM_TOPDIR/SPECS/decisionengine.spec

rpm_dirs="BUILD RPMS SOURCES SPECS SRPMS"

for dir in $rpm_dirs
do
    d=$RPM_TOPDIR/$dir
    echo "Creating dir: $d"
    mkdir -p $d
done

rm -rf $release_dir
mkdir -p $product_release_dir

cp -r $source_dir/*  $product_release_dir
cd $release_dir
tar --exclude=.git --exclude=.gitignore --exclude=doc --exclude=cxx/build \
    --exclude=readme --exclude=.cache --exclude=Dockerfile* --exclude=requirements.txt \
    --exclude=decisionengine/decisionengine \
    -czf $release_tar decisionengine

cp $release_tar $RPM_TOPDIR/SOURCES
cp $spec_template $RPM_TOPDIR/SPECS

rpmbuild -bs $spec_file
rpmbuild -bb $spec_file

#mock -r epel-el7-x86_64 --macro-file=$rpm_macros -i python
#mock --no-clean -r epel-el7-x86_64 --macro-file=%s --resultdir=%s/RPMS rebuild %s

#mock --macro-file=$rpm_macros -i python
#mock --no-clean --macro-file=$rpm_macros --resultdir=$RPM_TOPDIR/RPMS rebuild $spec_file

echo "========================================================================="
echo "RESULTS"
echo "========================================================================="
echo
echo "DIRECTORY:"
echo "---------"
ls -latrd $RPM_TOPDIR
echo
echo "SOURCES:"
echo "-------"
ls -latrh $RPM_TOPDIR/SOURCES
echo
echo "SRPMS:"
echo "-----"
ls -latrh $RPM_TOPDIR/SRPMS
echo
echo "RPMS:"
echo "----"
ls -latrh $RPM_TOPDIR/RPMS/x86_64
echo "_________________________________________________________________________"
