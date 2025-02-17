# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# RPM package for HEPCloud DEcisionengine pre-requisites

# Disable shebang mangling (see GHI#436)
%undefine __brp_mangle_shebangs

# python3 == python3.9
%global python3_pkgversion 3

# Versions use semantic versioning (M.m.p)
# Release Candidates NVR format
# define release 0.1.rc1
# Official Release NVR format
# define release 2

%define auto_version %(FULLVER=$(git describe --tag | sed 's/-/_/g');  GVER=$(sed 's/.*_\\\([[:digit:]].*\\\)_/dev\\\1+/g' <<< ${FULLVER}); VER=${FULLVER//_*}; echo ${VER%.*}.$((${VER##*.}+1)).${GVER})
%define auto_release 1

%define version __HCDE_RPM_VERSION__
%define release __HCDE_RPM_RELEASE__

%define decisionengine_home %{_sharedstatedir}/decisionengine
%define systemddir %{_prefix}/lib/systemd/system

Name:           decisionengine
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        HEPCloud DecisionEngine
License:        Apache-2.0
URL:            https://hepcloud.github.io/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
Prefix:         %{_prefix}
Vendor:         Fermilab <None>

Source:         hepcloud.tar.gz
Source1:        decision_engine.jsonnet

BuildRequires: python%{python3_pkgversion} >= 3.9
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: git
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: swig
#BuildRequires: python3-setuptools python3-wheel rpm-build

%description
The HEPCloud DecisionEngine provides a simple way to access the Grid, Cloud and HPC
resources through a dynamic HTCondor pool of grid-submitted resources.
It allows resource scheduling for disparate resource providers, including those
which may have a cost or a restricted allocation of cycles.

HEPCloud DecisionEngine is installed via PIP.
These RPMs provide all the pre-requisites and necessary setup.

Code documentation, release notes and install instructions are on github.io:
https://hepcloud.github.io/

#shadow-utils systemd python3.9dist(pip) python3.9dist(setuptools) python3.9dist(wheel) gcc gcc-c++ make python3.9-devel podman glideinwms-vofrontend-core glideinwms-vofrontend-glidein glideinwms-vofrontend-httpd glideinwms-vofrontend-libs glideinwms-userschedd glideinwms-usercollector


%package deps
Summary: The HEPCloud Decision Engine dependencies.
Requires: python%{python3_pkgversion} >= 3.9
# These were form the python packaging
Requires: shadow-utils
Requires: systemd
#Requires: python3.9dist(pip)
#Requires: python3.9dist(setuptools)
#Requires: python3.9dist(wheel)
# end form the python packaging
Requires: postgresql
Requires: postgresql-server
Requires: postgresql-devel
Requires: httpd
Requires: podman
Requires: python3-cryptography
Requires: python3-pip
Requires: gettext
# Required to build jsonnet (make, g++, and Python.h) (TODO: put in pip a build for jsonnet)
Requires: make
Requires: gcc-c++
Requires: python3-devel
%description deps
This subpackage includes all the RPM dependencied for the HEPCloud Decision Engine Framework.


%package modules-deps
Summary: The HEPCloud Decision Engine Modules dependencies.
Requires: python%{python3_pkgversion} >= 3.9
Requires: decisionengine-deps = %{version}-%{release}
Requires: glideinwms-vofrontend-libs
Requires: glideinwms-vofrontend-glidein
Requires: glideinwms-vofrontend-core
Requires: glideinwms-vofrontend-httpd
%description modules-deps
This subpackage includes all the RPM dependencied for the HEPCloud Decision Engine Modules.


%package onenode
Summary: The HEPCloud Decision Engine Framework and Modules dependencies, and extra-services.
Requires: decisionengine-deps = %{version}-%{release}
Requires: decisionengine-modules-deps = %{version}-%{release}
# These may actually be on another host
Requires: glideinwms-userschedd
Requires: glideinwms-usercollector
%description onenode
This subpackage includes all the RPM dependencies for the HEPCloud Decision Engine Framework and Modules and additional used services.


%prep
# Empty for now
%setup -q -n hepcloud
# Apply the patches here if any
#%patch -P 0 -p1


%build
#cp %{SOURCE7} .
#chmod 700 chksum.sh

%install
rm -rf $RPM_BUILD_ROOT

# Set the Python version
%global __python %{__python3}

# TODO: Check if some of the following are needed
# seems never used
# %define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

# From http://fedoraproject.org/wiki/Packaging:Python
# Assuming python3_sitelib and python3_sitearch are defined, not supporting RHEL < 7 or old FC
# Define python_sitelib


#Create the RPM startup files (init.d) from the templates
#creation/create_rpm_startup . decisionengine_initd_startup_template %{SOURCE2}

# Create some directories
install -d $RPM_BUILD_ROOT%{decisionengine_home}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/decisionengine
install -d $RPM_BUILD_ROOT%{_sysconfdir}/decisionengine/config.d
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/decisionengine
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/decisionengine/

%clean
rm -rf $RPM_BUILD_ROOT


%pre deps
# Add the "decisionengine" user and group if they do not exist
getent group decisionengine >/dev/null || groupadd -r decisionengine
getent passwd decisionengine >/dev/null || \
       useradd -r -g decisionengine -d %{decisionengine_home} \
	-c "HEPCloud Decision Engine user" -s /sbin/nologin decisionengine
# If the decisionengine user already exists make sure it is part of decisionengine group
usermod --append --groups decisionengine decisionengine >/dev/null


%post deps
# make sure our home area makes sense since we have a dynamic id
chown decisionengine:decisionengine %{decisionengine_home}
chmod 750 %{decisionengine_home}

# If the decisionengine user already exists make sure it is part of
# the decisionengine group
usermod --append --groups decisionengine decisionengine >/dev/null

# Change the ownership of log and lock dir if they already exist
if [ -d %{_localstatedir}/log/decisionengine ]; then
    chown -R decisionengine:decisionengine %{_localstatedir}/log/decisionengine
fi

systemctl daemon-reload


%postun deps
systemctl daemon-reload


%files deps
%defattr(-,decisionengine,decisionengine,-)
%dir %{decisionengine_home}
%dir %{_sysconfdir}/decisionengine
%dir %{_sysconfdir}/decisionengine/config.d
%config(noreplace) %{_sysconfdir}/decisionengine/decision_engine.jsonnet
# add all files in config.d
%attr(-, decisionengine, decisionengine) %dir %{_localstatedir}/log/decisionengine

%files modules-deps
