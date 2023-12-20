# The is a parameter "_dedir" that is used in the install section.
# To build the RPM it is needed to run the following command from inside the decisionengine code folder:
#  rpmbuild --define "_dedir $(pwd)" -bb package/rpm/decisionengine-deps.spec

%define name decisionengine-deps
# to get the version set properly the "rpmbuild" command needs to be executed from inside the decisionengine repo folder
%define version %(FULLVER=$(git describe --tag | sed 's/-/_/g');  GVER=$(sed 's/.*_\\\([[:digit:]].*\\\)_/dev\\\1+/g' <<< ${FULLVER}); VER=${FULLVER//_*}; echo ${VER%.*}.$((${VER##*.}+1)).${GVER})
%define release 1%{?dist}
%define pwd %(echo $(pwd))

Summary: The HEPCloud Decision Engine Framework
Name: %{name}
Version: %{version}
Release: %{release}
License: Apache-2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Fermilab <None>
Requires: shadow-utils systemd python3.9dist(pip) python3.9dist(setuptools) python3.9dist(wheel) gcc gcc-c++ make python3.9-devel glideinwms-vofrontend-core glideinwms-vofrontend-glidein glideinwms-vofrontend-httpd glideinwms-vofrontend-libs glideinwms-userschedd glideinwms-usercollector
Url: http://hepcloud.fnal.gov/

%description
<!--
SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
SPDX-License-Identifier: Apache-2.0
-->

# HEPCloud Decision Engine

The Decision Engine is a critical component of the HEP Cloud Facility. It provides the
functionality of resource scheduling for disparate resource providers, including those
which may have a cost or a restricted allocation of cycles

Code documentation, release notes and install instructions are on github.io:
https://hepcloud.github.io/decisionengine/

# Getting Started with development

There is a specfic document on this at https://github.com/HEPCloud/decisionengine/blob/master/DEVELOPMENT.md


%prep


%build


%install
mkdir -p %{buildroot}/%{_localstatedir}/log/decisionengine
echo "%attr(0750,decisionengine,decisionengine) %{_localstatedir}/log/decisionengine" > INSTALLED_FILES

mkdir -p %{buildroot}/%{_sharedstatedir}/decisionengine
echo "%attr(0750,decisionengine,decisionengine) %{_sharedstatedir}/decisionengine" >> INSTALLED_FILES

mkdir -p %{buildroot}/%{_sysconfdir}/decisionengine/config.d
cp -r %{_dedir}/config/* %{buildroot}/%{_sysconfdir}/decisionengine/

echo "%dir %attr(0750,decisionengine,decisionengine) %{_sysconfdir}/decisionengine/" >> INSTALLED_FILES
echo "%attr(0640,decisionengine,decisionengine) %config(noreplace) %{_sysconfdir}/decisionengine/decision_engine.jsonnet" >> INSTALLED_FILES

echo "%dir %attr(0750,decisionengine,decisionengine) %{_sysconfdir}/decisionengine/config.d/" >> INSTALLED_FILES
[ "$(ls -A %{buildroot}/%{_sysconfdir}/decisionengine/config.d)" ] && echo "%attr(0640decisionengine,decisionengine) %config(noreplace) %{_sysconfdir}/decisionengine/config.d/*" >> INSTALLED_FILES


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "decisionengine" user and group if they do not exist
#
# eventually this should be systemd-sysusers, but not on EL7
getent group decisionengine >/dev/null ||
    groupadd -r  decisionengine
getent passwd  decisionengine >/dev/null || \
    useradd -r -g  decisionengine -d %{_sharedstatedir}/decisionengine \
    -c "Decision Engine user" -s /sbin/nologin -m decisionengine


%post
# make sure our home area makes sense since we have a dynamic id
chown decisionengine:decisionengine %{_sharedstatedir}/decisionengine
chmod 750 %{_sharedstatedir}/decisionengine

# If the decisionengine user already exists make sure it is part of
# the decisionengine group
usermod --append --groups  decisionengine  decisionengine >/dev/null

# Change the ownership of log and lock dir if they already exist
if [ -d %{_localstatedir}/log/decisionengine ]; then
    chown -R decisionengine:decisionengine %{_localstatedir}/log/decisionengine
fi

systemctl daemon-reload


%postun
systemctl daemon-reload

%files
/etc/
/var/
